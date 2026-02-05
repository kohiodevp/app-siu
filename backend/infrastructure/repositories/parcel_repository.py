"""
Implémentation des repositories SQLAlchemy
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, exc as sql_exceptions
from backend.core.repository_interfaces import IParcelRepository
from backend.models.parcel import Parcel
from backend.utils.db_helpers import safe_ilike


class SqlParcelRepository(IParcelRepository):
    """
    Implémentation SQLAlchemy du repository des parcelles
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[Parcel]:
        try:
            return self.db_session.query(Parcel)\
                .options(joinedload(Parcel.owner), joinedload(Parcel.creator))\
                .filter(Parcel.id == id)\
                .first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de la parcelle par ID: {e}")
            return None

    def get_by_reference(self, reference: str) -> Optional[Parcel]:
        try:
            return self.db_session.query(Parcel).filter(Parcel.reference_cadastrale == reference).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de la parcelle par référence: {e}")
            return None

    def get_all(self) -> List[Parcel]:
        try:
            return self.db_session.query(Parcel).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de toutes les parcelles: {e}")
            return []

    def get_by_owner(self, owner_id: str) -> List[Parcel]:
        try:
            return self.db_session.query(Parcel).filter(Parcel.owner_id == owner_id).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des parcelles par propriétaire: {e}")
            return []

    def create(self, parcel: Parcel) -> Parcel:
        try:
            self.db_session.add(parcel)
            self.db_session.flush()  # Pour obtenir l'ID si nécessaire
            return parcel
        except sql_exceptions.IntegrityError as e:
            self.db_session.rollback()
            raise e
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de la parcelle: {e}")
            raise e

    def update(self, id: str, parcel: Parcel) -> Optional[Parcel]:
        try:
            existing_parcel = self.get_by_id(id)
            if existing_parcel:
                # Mettre à jour les champs
                existing_parcel.coordinates_lat = parcel.coordinates_lat
                existing_parcel.coordinates_lng = parcel.coordinates_lng
                existing_parcel.area = parcel.area
                existing_parcel.address = parcel.address
                existing_parcel.category = parcel.category
                existing_parcel.description = parcel.description
                existing_parcel.owner_id = parcel.owner_id
                existing_parcel.cadastral_plan_ref = parcel.cadastral_plan_ref
                existing_parcel.status = parcel.status
                existing_parcel.zone = parcel.zone
                existing_parcel.geometry = parcel.geometry
                existing_parcel.updated_at = parcel.updated_at

                return existing_parcel
            return None
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de la parcelle: {e}")
            raise e

    def delete(self, id: str) -> bool:
        try:
            parcel = self.get_by_id(id)
            if parcel:
                self.db_session.delete(parcel)
                return True
            return False
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la suppression de la parcelle: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[Parcel]:
        try:
            query = self.db_session.query(Parcel)

            # Appliquer les filtres de recherche
            search_term = criteria.get('search_term')
            reference = criteria.get('reference_cadastrale')
            address = criteria.get('address')
            owner_id = criteria.get('owner_id')
            category = criteria.get('category')
            page = criteria.get('page', 1)
            page_size = criteria.get('page_size', 100)

            if reference:
                query = query.filter(safe_ilike(Parcel.reference_cadastrale, reference))

            if search_term:
                query = query.filter(or_(
                    safe_ilike(Parcel.reference_cadastrale, search_term),
                    safe_ilike(Parcel.address, search_term),
                    safe_ilike(Parcel.description, search_term)
                ))

            if address:
                query = query.filter(safe_ilike(Parcel.address, address))

            if owner_id:
                query = query.filter(Parcel.owner_id == owner_id)

            if category:
                query = query.filter(Parcel.category == category)

            # Trier par date de création décroissante
            query = query.order_by(Parcel.created_at.desc())

            # Pagination
            offset = (page - 1) * page_size
            return query.limit(page_size).offset(offset).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des parcelles: {e}")
            return []
    
    def count_search(self, criteria: Dict[str, Any]) -> int:
        """Compte le nombre total de résultats pour une recherche"""
        try:
            query = self.db_session.query(Parcel)

            # Appliquer les mêmes filtres que search()
            search_term = criteria.get('search_term')
            reference = criteria.get('reference_cadastrale')
            address = criteria.get('address')
            owner_id = criteria.get('owner_id')
            category = criteria.get('category')

            if reference:
                query = query.filter(safe_ilike(Parcel.reference_cadastrale, reference))

            if search_term:
                query = query.filter(or_(
                    safe_ilike(Parcel.reference_cadastrale, search_term),
                    safe_ilike(Parcel.address, search_term),
                    safe_ilike(Parcel.description, search_term)
                ))

            if address:
                query = query.filter(safe_ilike(Parcel.address, address))

            if owner_id:
                query = query.filter(Parcel.owner_id == owner_id)

            if category:
                query = query.filter(Parcel.category == category)

            return query.count()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors du comptage des parcelles: {e}")
            return 0

    def get_with_filters(self, filters: Dict[str, Any]) -> List[Parcel]:
        try:
            query = self.db_session.query(Parcel)

            # Appliquer les filtres génériques
            for attr, value in filters.items():
                if hasattr(Parcel, attr):
                    column = getattr(Parcel, attr)
                    if isinstance(value, (list, tuple)):
                        # Si la valeur est une liste, utiliser IN
                        query = query.filter(column.in_(value))
                    else:
                        # Sinon, utiliser l'égalité
                        query = query.filter(column == value)

            return query.all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des parcelles avec filtres: {e}")
            return []