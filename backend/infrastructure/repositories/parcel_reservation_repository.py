"""
Implémentation du repository pour les réservations de parcelles.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, exc as sql_exceptions
from datetime import datetime
from backend.core.repository_interfaces import IParcelReservationRepository
from backend.models.availability import ParcelReservation


class SqlParcelReservationRepository(IParcelReservationRepository):
    """
    Implémentation SQLAlchemy du repository des réservations de parcelles.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[ParcelReservation]:
        try:
            return self.db_session.query(ParcelReservation).filter(ParcelReservation.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de la réservation par ID: {e}")
            return None

    def get_all(self) -> List[ParcelReservation]:
        try:
            return self.db_session.query(ParcelReservation).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de toutes les réservations: {e}")
            return []

    def create(self, entity: ParcelReservation) -> ParcelReservation:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de la réservation: {e}")
            raise e

    def update(self, id: str, entity: ParcelReservation) -> Optional[ParcelReservation]:
        try:
            existing = self.get_by_id(id)
            if existing:
                # Mettre à jour les champs si nécessaire
                existing.is_active = entity.is_active
                return existing
            return None
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de la réservation: {e}")
            raise e

    def delete(self, id: str) -> bool:
        try:
            entity = self.get_by_id(id)
            if entity:
                self.db_session.delete(entity)
                return True
            return False
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la suppression de la réservation: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[ParcelReservation]:
        try:
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des réservations: {e}")
            return []

    def get_active_reservation(self, parcel_id: str) -> Optional[ParcelReservation]:
        """
        Récupère la réservation active pour une parcelle.
        """
        try:
            now = datetime.now()
            return self.db_session.query(ParcelReservation).filter(
                and_(
                    ParcelReservation.parcel_id == parcel_id,
                    ParcelReservation.status == 'active',  # Using status instead of is_active
                    ParcelReservation.expires_at > now
                )
            ).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de la réservation active: {e}")
            return None
