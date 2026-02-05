"""
Service de gestion des documents
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.core.repository_interfaces import IDocumentRepository, IUserRepository, IParcelRepository
from backend.models.document import Document
from backend.models.user import User
from backend.models.parcel import Parcel


class DocumentService:
    """
    Service pour la gestion des documents
    """
    
    def __init__(
        self,
        document_repository: IDocumentRepository,
        user_repository: IUserRepository,
        parcel_repository: IParcelRepository
    ):
        self.document_repository = document_repository
        self.user_repository = user_repository
        self.parcel_repository = parcel_repository

    def search_in_documents(self, query: str, parcel_id: Optional[str] = None, document_type: Optional[str] = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Recherche dans le texte des documents
        """
        filters = {
            'search_query': query,
            'parcel_id': parcel_id,
            'document_type': document_type
        }
        
        # Supprimer les valeurs None
        filters = {k: v for k, v in filters.items() if v is not None}
        
        results = self.document_repository.search_with_text_content(filters, page, page_size)
        
        return {
            'items': [self._document_to_dict(doc) for doc in results['items']],
            'total': results['total'],
            'page': results['page'],
            'page_size': results['page_size'],
            'total_pages': results['total_pages']
        }

    def generate_preview(self, document_id: str, page: int = 1) -> bytes:
        """
        Génère un aperçu d'un document
        """
        # Pour l'instant, on simule la génération d'un aperçu
        # En production, on utiliserait une bibliothèque comme Pillow ou Wand
        import io
        from PIL import Image, ImageDraw
        
        # Créer une image de prévisualisation simple
        img = Image.new('RGB', (400, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"Aperçu du document {document_id}", fill=(0, 0, 0))
        draw.text((10, 30), f"Page {page}", fill=(0, 0, 0))
        
        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()

    def generate_thumbnail(self, document_id: str, width: int = 200, height: int = 200) -> bytes:
        """
        Génère une miniature d'un document
        """
        import io
        from PIL import Image, ImageDraw
        
        # Créer une miniature simple
        img = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        draw.rectangle([5, 5, width-5, height-5], outline=(100, 100, 100), width=2)
        draw.text((width//2 - 30, height//2 - 10), "PDF", fill=(100, 100, 100))
        
        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        return buffer.getvalue()

    def extract_text(self, document_id: str) -> Dict[str, str]:
        """
        Extrait le texte d'un document (OCR)
        """
        # Pour l'instant, on simule l'extraction de texte
        # En production, on utiliserait une bibliothèque comme pytesseract ou pdfplumber
        document = self.document_repository.get_by_id(document_id)
        if not document:
            return {'error': 'Document non trouvé', 'text': ''}
        
        # Simuler l'extraction de texte
        sample_text = f"Texte extrait du document {document.filename} - Référence: {document.reference}\nContenu du document..."
        
        return {
            'document_id': document_id,
            'text': sample_text,
            'pages_count': 1
        }

    def analyze_document(self, document_id: str) -> Dict[str, Any]:
        """
        Analyse un document pour extraction d'informations
        """
        document = self.document_repository.get_by_id(document_id)
        if not document:
            return {'error': 'Document non trouvé'}
        
        # Simuler l'analyse du document
        analysis = {
            'document_id': document_id,
            'file_type': document.mime_type,
            'file_size': document.file_size,
            'pages': 1,  # Simulé
            'detected_language': 'French',  # Simulé
            'entities': [
                {'type': 'DATE', 'value': '2023-01-01', 'confidence': 0.95},
                {'type': 'LOCATION', 'value': 'Ouagadougou', 'confidence': 0.92},
                {'type': 'PERSON', 'value': 'Jean Dupont', 'confidence': 0.88}
            ],
            'keywords': ['foncier', 'parcelle', 'titre', 'propriété', 'cadastrale'],
            'classification': 'Titre de propriété',  # Simulé
            'confidence': 0.90
        }
        
        return analysis

    def get_popular_tags(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Récupère les tags les plus populaires
        """
        # Pour l'instant, on simule les tags populaires
        # En production, on récupérerait les tags réels des documents
        popular_tags = [
            {'tag': 'titre_propriete', 'count': 125},
            {'tag': 'plan_cadastral', 'count': 98},
            {'tag': 'autorisation_construction', 'count': 76},
            {'tag': 'contrat_vente', 'count': 65},
            {'tag': 'certificat_heritage', 'count': 43},
            {'tag': 'document_fiscal', 'count': 38},
            {'tag': 'document_technique', 'count': 32},
            {'tag': 'document_administratif', 'count': 29}
        ]
        
        return popular_tags[:limit]

    def search_by_tags(self, tags: List[str], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Recherche des documents par tags
        """
        # Rechercher les documents avec les tags spécifiés
        filters = {'tags': tags}
        results = self.document_repository.search_by_tags(filters, page, page_size)
        
        return {
            'items': [self._document_to_dict(doc) for doc in results['items']],
            'total': results['total'],
            'page': results['page'],
            'page_size': results['page_size'],
            'total_pages': results['total_pages']
        }

    def validate_document(self, document_id: str) -> Dict[str, Any]:
        """
        Valide un document
        """
        document = self.document_repository.get_by_id(document_id)
        if not document:
            return {'valid': False, 'errors': ['Document non trouvé']}
        
        # Simuler la validation du document
        errors = []
        
        # Vérifier le format
        if not self._is_valid_format(document.mime_type):
            errors.append('Format de document non supporté')
        
        # Vérifier la taille
        if document.file_size > 50 * 1024 * 1024:  # 50MB
            errors.append('Taille de fichier trop importante')
        
        # Vérifier le nom de fichier
        if not self._is_valid_filename(document.filename):
            errors.append('Nom de fichier invalide')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def sign_document(self, document_id: str, signature: str) -> Dict[str, Any]:
        """
        Signe numériquement un document
        """
        document = self.document_repository.get_by_id(document_id)
        if not document:
            return {'signed': False, 'error': 'Document non trouvé'}
        
        # Simuler la signature numérique
        # En production, on utiliserait une bibliothèque de signature numérique
        document.signature = signature
        document.signed_at = datetime.now()
        document.is_signed = True
        
        updated_document = self.document_repository.update(document_id, document)
        
        return {
            'signed': True,
            'signature_id': f"sig_{document_id}_{int(datetime.now().timestamp())}",
            'document': self._document_to_dict(updated_document)
        }

    def verify_signature(self, document_id: str) -> Dict[str, Any]:
        """
        Vérifie la signature d'un document
        """
        document = self.document_repository.get_by_id(document_id)
        if not document or not document.is_signed:
            return {'valid': False, 'error': 'Document non signé ou non trouvé'}
        
        # Simuler la vérification de signature
        # En production, on utiliserait une bibliothèque de vérification de signature
        return {
            'valid': True,
            'signer': 'Système de signature',
            'timestamp': document.signed_at.isoformat() if document.signed_at else None,
            'signature_algorithm': 'RSA-256'
        }

    def add_annotations(self, document_id: str, annotations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ajoute des annotations à un document
        """
        document = self.document_repository.get_by_id(document_id)
        if not document:
            return {'success': False, 'error': 'Document non trouvé'}
        
        # Ajouter les annotations au document
        if not hasattr(document, 'annotations') or document.annotations is None:
            document.annotations = []
        
        for annotation in annotations:
            annotation['id'] = f"ann_{len(document.annotations) + 1}"
            annotation['created_at'] = datetime.now()
            document.annotations.append(annotation)
        
        updated_document = self.document_repository.update(document_id, document)
        
        return {
            'success': True,
            'document_id': document_id,
            'annotation_count': len(document.annotations)
        }

    def get_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Récupère les annotations d'un document
        """
        document = self.document_repository.get_by_id(document_id)
        if not document or not hasattr(document, 'annotations') or document.annotations is None:
            return []
        
        return document.annotations

    def compare_documents(self, doc_id1: str, doc_id2: str) -> Dict[str, Any]:
        """
        Compare deux documents
        """
        doc1 = self.document_repository.get_by_id(doc_id1)
        doc2 = self.document_repository.get_by_id(doc_id2)
        
        if not doc1 or not doc2:
            return {'error': 'Un ou les deux documents sont introuvables'}
        
        # Simuler la comparaison de documents
        # En production, on utiliserait une bibliothèque de comparaison de documents
        return {
            'similarity': 0.85,  # Pourcentage de similarité
            'differences': [
                {
                    'type': 'content_difference',
                    'description': 'Différence dans le contenu',
                    'page': 1
                }
            ],
            'common_elements': ['header', 'footer', 'title'],
            'unique_to_doc1': ['clause_spécifique_1'],
            'unique_to_doc2': ['clause_spécifique_2']
        }

    def _is_valid_format(self, mime_type: str) -> bool:
        """
        Vérifie si le format est valide
        """
        valid_formats = [
            'application/pdf',
            'image/jpeg', 'image/jpg', 'image/png', 'image/tiff',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        return mime_type in valid_formats

    def _is_valid_filename(self, filename: str) -> bool:
        """
        Vérifie si le nom de fichier est valide
        """
        import re
        # Vérifier qu'il n'y a pas de caractères dangereux
        pattern = r'^[\w\-. ]+\.\w+$'
        return bool(re.match(pattern, filename))

    def _document_to_dict(self, document: Document) -> Dict[str, Any]:
        """
        Convertit un document en dictionnaire
        """
        return {
            'id': document.id,
            'filename': document.filename,
            'original_filename': document.original_filename,
            'file_path': document.file_path,
            'file_size': document.file_size,
            'mime_type': document.mime_type,
            'parcel_id': document.parcel_id,
            'document_type': document.document_type.value if hasattr(document.document_type, 'value') else str(document.document_type),
            'version': document.version,
            'is_public': document.is_public,
            'is_signed': getattr(document, 'is_signed', False),
            'signed_at': getattr(document, 'signed_at', None),
            'signature': getattr(document, 'signature', None),
            'deleted': document.deleted,
            'description': document.description,
            'uploaded_by': document.uploaded_by,
            'uploaded_at': document.uploaded_at.isoformat() if hasattr(document.uploaded_at, 'isoformat') else str(document.uploaded_at),
            'created_at': document.created_at.isoformat() if hasattr(document.created_at, 'isoformat') else str(document.created_at),
            'updated_at': document.updated_at.isoformat() if hasattr(document.updated_at, 'isoformat') else str(document.updated_at)
        }