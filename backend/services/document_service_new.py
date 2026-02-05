"""
DocumentService - Gestion complète des documents
Version améliorée avec validation, sécurité, thumbnails, et métadonnées complètes
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, BinaryIO
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Import des services
from .storage_service import StorageService
from .document_validator import DocumentValidator

# Import des modèles (à adapter selon votre structure)
# from backend.models.document import Document, DocumentType, DocumentStatus
# from backend.models.user import User

# Configuration
UPLOAD_BASE_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
MAX_FILE_SIZE_MB = int(os.environ.get('MAX_FILE_SIZE_MB', '50'))


class DocumentService:
    """Service complet pour la gestion des documents"""
    
    def __init__(self, db_session: Session):
        """
        Initialize document service
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.storage = StorageService(UPLOAD_BASE_FOLDER)
        self.validator = DocumentValidator(MAX_FILE_SIZE_MB)
    
    def upload_document(
        self, 
        file: BinaryIO, 
        parcel_id: int, 
        title: str,
        filename: str,
        document_type: str,
        uploaded_by: int,
        description: str = "",
        tags: list = None,
        expiry_date: datetime = None
    ) -> Dict[str, Any]:
        """
        Upload un document avec validation complète
        
        Args:
            file: Fichier à uploader (file object)
            parcel_id: ID de la parcelle
            title: Titre du document
            filename: Nom du fichier original
            document_type: Type de document
            uploaded_by: ID de l'utilisateur
            description: Description optionnelle
            tags: Liste de tags
            expiry_date: Date d'expiration optionnelle
            
        Returns:
            dict: Résultat avec document créé ou erreur
        """
        try:
            # 1. Lire les données du fichier
            file.seek(0)
            file_data = file.read()
            
            # 2. Valider le fichier
            is_valid, error_msg, mime_type = self.validator.validate_file(file_data, filename)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # 3. Sanitize filename
            safe_filename = self.validator.sanitize_filename(filename)
            
            # 4. Créer le document en DB pour obtenir un ID
            from backend.models.document import Document, DocumentStatus
            
            document = Document(
                parcel_id=parcel_id,
                title=title,
                description=description,
                document_type=document_type,
                filename=safe_filename,
                mime_type=mime_type,
                file_size=len(file_data),
                uploaded_by=uploaded_by,
                tags=json.dumps(tags) if tags else None,
                expiry_date=expiry_date,
                status=DocumentStatus.EN_ATTENTE
            )
            
            self.db.add(document)
            self.db.flush()  # Pour obtenir l'ID
            
            # 5. Sauvegarder le fichier sur disque
            file.seek(0)
            file_path, checksum, file_size = self.storage.save_document(
                file, parcel_id, document.id, safe_filename
            )
            
            # 6. Mettre à jour le document avec les infos de stockage
            document.file_path = file_path
            document.checksum = checksum
            document.file_size = file_size
            
            # 7. Générer thumbnail si c'est une image
            if mime_type.startswith('image/'):
                thumbnail_data = self.validator.generate_thumbnail(file_data)
                if thumbnail_data:
                    thumbnail_path = self.storage.save_thumbnail(
                        thumbnail_data, parcel_id, document.id
                    )
                    document.thumbnail_path = thumbnail_path
            
            # 8. Commit
            self.db.commit()
            
            return {
                'success': True,
                'document': document.to_dict(),
                'message': 'Document uploadé avec succès'
            }
            
        except Exception as e:
            self.db.rollback()
            return {
                'success': False,
                'error': f'Erreur lors de l\'upload : {str(e)}'
            }
    
    def upload_multiple_documents(
        self,
        files: list[tuple[BinaryIO, str]],  # (file, filename)
        parcel_id: int,
        document_type: str,
        uploaded_by: int
    ) -> Dict[str, Any]:
        """
        Upload multiple documents à la fois
        
        Returns:
            dict: Résultat avec liste des documents créés et erreurs
        """
        results = {
            'success': True,
            'documents': [],
            'errors': []
        }
        
        for file, filename in files:
            result = self.upload_document(
                file=file,
                parcel_id=parcel_id,
                title=filename,
                filename=filename,
                document_type=document_type,
                uploaded_by=uploaded_by
            )
            
            if result['success']:
                results['documents'].append(result['document'])
            else:
                results['errors'].append({
                    'filename': filename,
                    'error': result['error']
                })
                results['success'] = False
        
        return results
    
    def get_document(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un document par son ID"""
        try:
            from backend.models.document import Document
            
            document = self.db.query(Document).filter(
                Document.id == document_id,
                Document.deleted == False
            ).first()
            
            if not document:
                return None
            
            # Mettre à jour last_accessed
            document.last_accessed = datetime.utcnow()
            self.db.commit()
            
            return document.to_dict()
            
        except Exception as e:
            print(f"Erreur get_document: {e}")
            return None
    
    def get_document_file(self, document_id: int) -> Optional[Path]:
        """Retourne le chemin du fichier pour téléchargement"""
        try:
            from backend.models.document import Document
            
            document = self.db.query(Document).filter(
                Document.id == document_id,
                Document.deleted == False
            ).first()
            
            if not document:
                return None
            
            file_path = self.storage.get_document_path(document.file_path)
            
            if not file_path.exists():
                return None
            
            # Vérifier l'intégrité
            if document.checksum:
                if not self.validator.check_file_integrity(file_path, document.checksum):
                    print(f"Alerte: Intégrité compromise pour document {document_id}")
                    return None
            
            return file_path
            
        except Exception as e:
            print(f"Erreur get_document_file: {e}")
            return None
    
    def list_documents_by_parcel(
        self,
        parcel_id: int,
        document_type: str = None,
        status: str = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Liste les documents d'une parcelle avec filtres
        
        Args:
            parcel_id: ID de la parcelle
            document_type: Filtrer par type (optionnel)
            status: Filtrer par statut (optionnel)
            limit: Limite de résultats
            offset: Offset pour pagination
            
        Returns:
            list: Liste de documents
        """
        try:
            from backend.models.document import Document
            
            query = self.db.query(Document).filter(
                Document.parcel_id == parcel_id,
                Document.deleted == False
            )
            
            if document_type:
                query = query.filter(Document.document_type == document_type)
            
            if status:
                query = query.filter(Document.status == status)
            
            documents = query.order_by(Document.uploaded_at.desc())\
                             .limit(limit)\
                             .offset(offset)\
                             .all()
            
            return [doc.to_dict() for doc in documents]
            
        except Exception as e:
            print(f"Erreur list_documents: {e}")
            return []
    
    def search_documents(
        self,
        query: str = None,
        parcel_id: int = None,
        document_type: str = None,
        tags: list = None,
        uploaded_by: int = None,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> List[Dict[str, Any]]:
        """
        Recherche avancée de documents
        
        Args:
            query: Recherche textuelle (titre, description)
            parcel_id: Filtrer par parcelle
            document_type: Filtrer par type
            tags: Filtrer par tags
            uploaded_by: Filtrer par utilisateur
            date_from: Date de début
            date_to: Date de fin
            
        Returns:
            list: Documents correspondants
        """
        try:
            from backend.models.document import Document
            
            filters = [Document.deleted == False]
            
            if query:
                search_filter = or_(
                    Document.title.contains(query),
                    Document.description.contains(query),
                    Document.filename.contains(query)
                )
                filters.append(search_filter)
            
            if parcel_id:
                filters.append(Document.parcel_id == parcel_id)
            
            if document_type:
                filters.append(Document.document_type == document_type)
            
            if uploaded_by:
                filters.append(Document.uploaded_by == uploaded_by)
            
            if date_from:
                filters.append(Document.uploaded_at >= date_from)
            
            if date_to:
                filters.append(Document.uploaded_at <= date_to)
            
            if tags:
                # Recherche dans le JSON
                for tag in tags:
                    filters.append(Document.tags.contains(tag))
            
            documents = self.db.query(Document)\
                              .filter(and_(*filters))\
                              .order_by(Document.uploaded_at.desc())\
                              .all()
            
            return [doc.to_dict() for doc in documents]
            
        except Exception as e:
            print(f"Erreur search_documents: {e}")
            return []
    
    def validate_document(
        self,
        document_id: int,
        validated_by: int,
        is_approved: bool,
        comment: str = None
    ) -> Dict[str, Any]:
        """
        Valide ou refuse un document
        
        Args:
            document_id: ID du document
            validated_by: ID du validateur
            is_approved: True pour valider, False pour refuser
            comment: Commentaire de validation
            
        Returns:
            dict: Résultat de la validation
        """
        try:
            from backend.models.document import Document, DocumentStatus
            
            document = self.db.query(Document).filter(
                Document.id == document_id,
                Document.deleted == False
            ).first()
            
            if not document:
                return {'success': False, 'error': 'Document non trouvé'}
            
            document.validated = is_approved
            document.validated_by = validated_by
            document.validated_at = datetime.utcnow()
            document.validation_comment = comment
            document.status = DocumentStatus.VALIDE if is_approved else DocumentStatus.REFUSE
            
            self.db.commit()
            
            return {
                'success': True,
                'document': document.to_dict(),
                'message': f"Document {'validé' if is_approved else 'refusé'}"
            }
            
        except Exception as e:
            self.db.rollback()
            return {'success': False, 'error': str(e)}
    
    def delete_document(
        self,
        document_id: int,
        deleted_by: int,
        permanent: bool = False
    ) -> Dict[str, Any]:
        """
        Supprime un document (soft ou hard delete)
        
        Args:
            document_id: ID du document
            deleted_by: ID de l'utilisateur qui supprime
            permanent: True pour suppression définitive
            
        Returns:
            dict: Résultat de la suppression
        """
        try:
            from backend.models.document import Document
            
            document = self.db.query(Document).filter(
                Document.id == document_id
            ).first()
            
            if not document:
                return {'success': False, 'error': 'Document non trouvé'}
            
            if permanent:
                # Suppression physique du fichier
                self.storage.delete_document(document.file_path)
                if document.thumbnail_path:
                    self.storage.delete_thumbnail(document.thumbnail_path)
                
                # Suppression de la DB
                self.db.delete(document)
            else:
                # Soft delete
                document.deleted = True
                document.deleted_at = datetime.utcnow()
                document.deleted_by = deleted_by
            
            self.db.commit()
            
            return {
                'success': True,
                'message': 'Document supprimé'
            }
            
        except Exception as e:
            self.db.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Retourne des statistiques sur le stockage"""
        return self.storage.get_storage_stats()
    
    def cleanup_orphan_files(self) -> Dict[str, Any]:
        """Nettoie les fichiers orphelins"""
        try:
            from backend.models.document import Document
            
            # Récupérer tous les chemins valides
            documents = self.db.query(Document).all()
            valid_paths = [doc.file_path for doc in documents]
            if documents and documents[0].thumbnail_path:
                valid_paths.extend([doc.thumbnail_path for doc in documents if doc.thumbnail_path])
            
            deleted_count = self.storage.cleanup_orphan_files(valid_paths)
            
            return {
                'success': True,
                'deleted_count': deleted_count,
                'message': f'{deleted_count} fichiers orphelins supprimés'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
