"""
Implémentation du repository pour l'historique des parcelles.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import exc as sql_exceptions
from backend.core.repository_interfaces import IParcelHistoryRepository
from backend.models.audit_log import ParcelHistory


class SqlParcelHistoryRepository(IParcelHistoryRepository):
    """
    Implémentation SQLAlchemy du repository de l'historique des parcelles.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[ParcelHistory]:
        try:
            return self.db_session.query(ParcelHistory).filter(ParcelHistory.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'historique par ID: {e}")
            return None

    def get_all(self) -> List[ParcelHistory]:
        try:
            return self.db_session.query(ParcelHistory).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tout l'historique: {e}")
            return []

    def create(self, entity: ParcelHistory) -> ParcelHistory:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de l'historique: {e}")
            raise e

    def update(self, id: str, entity: ParcelHistory) -> Optional[ParcelHistory]:
        try:
            # L'historique est généralement immuable, mais on peut implémenter si nécessaire
            existing_history = self.get_by_id(id)
            if existing_history:
                # Mettre à jour les champs si nécessaire
                pass
            return existing_history
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de l'historique: {e}")
            raise e

    def delete(self, id: str) -> bool:
        try:
            history_entry = self.get_by_id(id)
            if history_entry:
                self.db_session.delete(history_entry)
                return True
            return False
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la suppression de l'historique: {e}")
            return False

    def delete_by_parcel_id(self, parcel_id: str):
        try:
            self.db_session.query(ParcelHistory).filter(ParcelHistory.parcel_id == parcel_id).delete()
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la suppression de l'historique par parcel_id: {e}")

    def search(self, criteria: dict) -> List[ParcelHistory]:
        try:
            # Implémenter la recherche si nécessaire
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche de l'historique: {e}")
            return []

    def get_by_parcel_id(self, parcel_id: str) -> List[ParcelHistory]:
        try:
            return self.db_session.query(ParcelHistory)\
                        .filter(ParcelHistory.parcel_id == parcel_id)\
                        .order_by(ParcelHistory.timestamp.desc())\
                        .all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'historique par parcel_id: {e}")
            return []
