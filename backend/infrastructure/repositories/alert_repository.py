"""
Implémentation du repository pour les alertes.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, exc as sql_exceptions

from backend.core.repository_interfaces import IAlertRepository
from backend.models.alert import Alert


class SqlAlertRepository(IAlertRepository):
    """
    Implémentation SQLAlchemy du repository des alertes.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[Alert]:
        try:
            return self.db_session.query(Alert).filter(Alert.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'alerte par ID: {e}")
            return None

    def get_all(self) -> List[Alert]:
        try:
            return self.db_session.query(Alert).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de toutes les alertes: {e}")
            return []

    def create(self, entity: Alert) -> Alert:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de l'alerte: {e}")
            raise e

    def update(self, id: str, entity: Alert) -> Optional[Alert]:
        try:
            existing = self.get_by_id(id)
            if existing:
                existing.acknowledged = entity.acknowledged
                existing.acknowledged_by = entity.acknowledged_by
                existing.acknowledged_at = entity.acknowledged_at
                return existing
            return None
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de l'alerte: {e}")
            raise e

    def delete(self, id: str) -> bool:
        return False  # Les alertes ne sont pas supprimées

    def search(self, criteria: Dict[str, Any]) -> List[Alert]:
        try:
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des alertes: {e}")
            return []

    def get_alerts(self, acknowledged: Optional[bool] = None, severity: Optional[str] = None, limit: int = 100) -> List[Alert]:
        """Get alerts with optional filtering"""
        try:
            query = self.db_session.query(Alert)

            if acknowledged is not None:
                query = query.filter(Alert.acknowledged == acknowledged)

            if severity:
                query = query.filter(Alert.severity == severity)

            return query.order_by(desc(Alert.created_at)).limit(limit).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des alertes: {e}")
            return []

    def get_alerts_for_parcel(self, parcel_id: str) -> List[Alert]:
        """Get all alerts for a specific parcel"""
        try:
            return self.db_session.query(Alert)\
                      .filter(Alert.parcel_id == parcel_id)\
                      .order_by(desc(Alert.created_at))\
                      .all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des alertes pour la parcelle: {e}")
            return []
