"""
Implémentation du repository pour les mutations foncières
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, and_, or_
from backend.core.repository_interfaces import IMutationRepository
from backend.models.mutation import ParcelMutation


class SqlMutationRepository(IMutationRepository):
    """
    Implémentation SQLAlchemy du repository des mutations foncières
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(ParcelMutation.id == id).first()
        except Exception as e:
            print(f"Erreur lors de la récupération de la mutation par ID: {e}")
            return None

    def get_all(self) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).all()
        except Exception as e:
            print(f"Erreur lors de la récupération de toutes les mutations: {e}")
            return []

    def create(self, entity: ParcelMutation) -> ParcelMutation:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except Exception as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de la mutation: {e}")
            raise e

    def update(self, id: str, entity: ParcelMutation) -> Optional[ParcelMutation]:
        try:
            existing = self.get_by_id(id)
            if existing:
                # Mettre à jour les champs de la mutation
                existing.parcel_id = entity.parcel_id
                existing.mutation_type = entity.mutation_type
                existing.from_owner_id = entity.from_owner_id
                existing.to_owner_id = entity.to_owner_id
                existing.initiated_by_user_id = entity.initiated_by_user_id
                existing.price = entity.price
                existing.notes = entity.notes
                existing.status = entity.status
                existing.approved_by_user_id = entity.approved_by_user_id
                existing.approved_at = entity.approved_at
                existing.completed_at = entity.completed_at
                existing.rejection_reason = entity.rejection_reason
                existing.updated_at = datetime.now()

                return existing
            return None
        except Exception as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de la mutation: {e}")
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
            print(f"Erreur lors de la suppression de la mutation: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[ParcelMutation]:
        try:
            query = self.db_session.query(ParcelMutation)

            # Appliquer les filtres
            if 'parcel_id' in criteria:
                query = query.filter(ParcelMutation.parcel_id == criteria['parcel_id'])
            if 'mutation_type' in criteria:
                query = query.filter(ParcelMutation.mutation_type == criteria['mutation_type'])
            if 'from_owner_id' in criteria:
                query = query.filter(ParcelMutation.from_owner_id == criteria['from_owner_id'])
            if 'to_owner_id' in criteria:
                query = query.filter(ParcelMutation.to_owner_id == criteria['to_owner_id'])
            if 'status' in criteria:
                query = query.filter(ParcelMutation.status == criteria['status'])
            if 'initiated_by_user_id' in criteria:
                query = query.filter(ParcelMutation.initiated_by_user_id == criteria['initiated_by_user_id'])
            if 'approved_by_user_id' in criteria:
                query = query.filter(ParcelMutation.approved_by_user_id == criteria['approved_by_user_id'])
            if 'from_date' in criteria:
                query = query.filter(ParcelMutation.created_at >= criteria['from_date'])
            if 'to_date' in criteria:
                query = query.filter(ParcelMutation.created_at <= criteria['to_date'])

            return query.all()
        except Exception as e:
            print(f"Erreur lors de la recherche des mutations: {e}")
            return []

    def get_by_parcel_id(self, parcel_id: str) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(ParcelMutation.parcel_id == parcel_id).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations par parcelle: {e}")
            return []

    def get_by_status(self, status: str) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(ParcelMutation.status == status).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations par statut: {e}")
            return []

    def get_by_type(self, mutation_type: str) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(ParcelMutation.mutation_type == mutation_type).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations par type: {e}")
            return []

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(
                and_(ParcelMutation.created_at >= start_date, ParcelMutation.created_at <= end_date)
            ).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations par plage de dates: {e}")
            return []

    def get_pending_mutations(self) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(
                ParcelMutation.status.in_(['pending', 'submitted', 'under_review'])
            ).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations en attente: {e}")
            return []

    def get_mutations_for_user(self, user_id: str) -> List[ParcelMutation]:
        try:
            return self.db_session.query(ParcelMutation).filter(
                or_(
                    ParcelMutation.initiated_by_user_id == user_id,
                    ParcelMutation.approved_by_user_id == user_id
                )
            ).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des mutations pour l'utilisateur: {e}")
            return []