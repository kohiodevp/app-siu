"""
Implémentation du repository pour les logs de vérification.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, exc as sql_exceptions
from backend.core.repository_interfaces import IVerificationLogRepository
from backend.models.availability import VerificationLog


class SqlVerificationLogRepository(IVerificationLogRepository):
    """
    Implémentation SQLAlchemy du repository des logs de vérification.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[VerificationLog]:
        try:
            return self.db_session.query(VerificationLog).filter(VerificationLog.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération du log de vérification par ID: {e}")
            return None

    def get_all(self) -> List[VerificationLog]:
        try:
            return self.db_session.query(VerificationLog).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tous les logs de vérification: {e}")
            return []

    def create(self, entity: VerificationLog) -> VerificationLog:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création du log de vérification: {e}")
            raise e

    def update(self, id: str, entity: VerificationLog) -> Optional[VerificationLog]:
        return None  # Les logs sont immuables

    def delete(self, id: str) -> bool:
        return False  # Les logs ne sont pas supprimés

    def search(self, criteria: Dict[str, Any]) -> List[VerificationLog]:
        try:
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des logs de vérification: {e}")
            return []

    def get_by_parcel_id(self, parcel_id: str, limit: int = 100) -> List[VerificationLog]:
        try:
            query = self.db_session.query(VerificationLog)
            if parcel_id:
                query = query.filter(VerificationLog.parcel_id == parcel_id)

            return query.order_by(desc(VerificationLog.check_timestamp)).limit(limit).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des logs de vérification par parcelle: {e}")
            return []

    def get_all_with_limit(self, limit: int = 100) -> List[VerificationLog]:
        try:
            return self.db_session.query(VerificationLog).order_by(desc(VerificationLog.check_timestamp)).limit(limit).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tous les logs de vérification avec limite: {e}")
            return []
