"""
Implémentation du repository pour les documents
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, and_, or_, func
from backend.core.repository_interfaces import IDocumentRepository
from backend.models.document import Document


class SqlDocumentRepository(IDocumentRepository):
    """
    Implémentation SQLAlchemy du repository des documents
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[Document]:
        try:
            return self.db_session.query(Document).filter(Document.id == id).first()
        except Exception as e:
            print(f"Erreur lors de la récupération du document par ID: {e}")
            return None

    def get_all(self) -> List[Document]:
        try:
            return self.db_session.query(Document).all()
        except Exception as e:
            print(f"Erreur lors de la récupération de tous les documents: {e}")
            return []

    def create(self, entity: Document) -> Document:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except Exception as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création du document: {e}")
            raise e

    def update(self, id: str, entity: Document) -> Optional[Document]:
        try:
            existing = self.get_by_id(id)
            if existing:
                # Mettre à jour les champs du document
                existing.filename = entity.filename
                existing.original_filename = entity.original_filename
                existing.file_path = entity.file_path
                existing.file_size = entity.file_size
                existing.mime_type = entity.mime_type
                existing.parcel_id = entity.parcel_id
                existing.document_type = entity.document_type
                existing.version = entity.version
                existing.is_public = entity.is_public
                existing.description = entity.description
                existing.uploaded_by = entity.uploaded_by
                existing.updated_at = datetime.now()
                
                return existing
            return None
        except Exception as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour du document: {e}")
            raise e

    def delete(self, id: str) -> bool:
        try:
            entity = self.get_by_id(id)
            if entity:
                self.db_session.delete(entity)
                return True
            return False
        except Exception as e:
            self.db_session.rollback()
            print(f"Erreur lors de la suppression du document: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[Document]:
        try:
            query = self.db_session.query(Document)
            
            # Appliquer les filtres
            if 'parcel_id' in criteria:
                query = query.filter(Document.parcel_id == criteria['parcel_id'])
            if 'document_type' in criteria:
                query = query.filter(Document.document_type == criteria['document_type'])
            if 'uploaded_by' in criteria:
                query = query.filter(Document.uploaded_by == criteria['uploaded_by'])
            if 'is_public' in criteria:
                query = query.filter(Document.is_public == criteria['is_public'])
            if 'from_date' in criteria:
                query = query.filter(Document.created_at >= criteria['from_date'])
            if 'to_date' in criteria:
                query = query.filter(Document.created_at <= criteria['to_date'])
            if 'search_term' in criteria:
                search_term = f"%{criteria['search_term']}%"
                query = query.filter(
                    or_(
                        Document.filename.ilike(search_term),
                        Document.original_filename.ilike(search_term),
                        Document.description.ilike(search_term)
                    )
                )
            
            # Tri
            sort_field = criteria.get('sort_field', 'created_at')
            sort_direction = criteria.get('sort_direction', 'desc')
            
            if sort_direction.lower() == 'asc':
                query = query.order_by(asc(getattr(Document, sort_field)))
            else:
                query = query.order_by(desc(getattr(Document, sort_field)))
            
            # Pagination
            page = criteria.get('page', 1)
            page_size = criteria.get('page_size', 10)
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
            
            return query.all()
        except Exception as e:
            print(f"Erreur lors de la recherche des documents: {e}")
            return []

    def get_by_parcel_id(self, parcel_id: str) -> List[Document]:
        try:
            return self.db_session.query(Document).filter(Document.parcel_id == parcel_id).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des documents par parcelle: {e}")
            return []

    def get_by_type(self, document_type: str) -> List[Document]:
        try:
            return self.db_session.query(Document).filter(Document.document_type == document_type).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des documents par type: {e}")
            return []

    def get_by_owner_id(self, owner_id: str) -> List[Document]:
        try:
            # On suppose que les documents sont liés aux parcelles qui ont des propriétaires
            # On devrait filtrer par les parcelles appartenant à l'owner
            from backend.models.parcel import Parcel
            parcel_ids = self.db_session.query(Parcel.id).filter(Parcel.owner_id == owner_id).all()
            parcel_id_list = [pid[0] for pid in parcel_ids]
            
            if not parcel_id_list:
                return []
                
            return self.db_session.query(Document).filter(Document.parcel_id.in_(parcel_id_list)).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des documents par propriétaire: {e}")
            return []

    def search_by_content(self, search_term: str) -> List[Document]:
        try:
            # Pour l'instant, on recherche dans les champs textuels
            # Dans une implémentation complète, on ferait une recherche dans le contenu des fichiers
            return self.db_session.query(Document).filter(
                or_(
                    Document.filename.ilike(f"%{search_term}%"),
                    Document.original_filename.ilike(f"%{search_term}%"),
                    Document.description.ilike(f"%{search_term}%")
                )
            ).all()
        except Exception as e:
            print(f"Erreur lors de la recherche dans le contenu des documents: {e}")
            return []

    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        try:
            return self.db_session.query(Document).order_by(desc(Document.created_at)).limit(limit).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des documents récents: {e}")
            return []

    def get_documents_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Document]:
        try:
            return self.db_session.query(Document).filter(
                and_(Document.created_at >= start_date, Document.created_at <= end_date)
            ).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des documents par plage de dates: {e}")
            return []

    def get_documents_by_tags(self, tags: List[str]) -> List[Document]:
        try:
            # Pour l'instant, on ne gère pas les tags dans le modèle Document
            # On retourne une liste vide
            # Dans une implémentation complète, on aurait une table de tags liée aux documents
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des documents par tags: {e}")
            return []