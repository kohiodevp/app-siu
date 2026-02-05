"""
Implémentation du repository pour les rôles.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import exc as sql_exceptions
from backend.core.repository_interfaces import IRoleRepository
from backend.models.user import Role


class SqlRoleRepository(IRoleRepository):
    """
    Implémentation SQLAlchemy du repository des rôles.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[Role]:
        try:
            return self.db_session.query(Role).filter(Role.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération du rôle par ID: {e}")
            return None

    def get_by_name(self, name: str) -> Optional[Role]:
        try:
            return self.db_session.query(Role).filter(Role.name == name.lower()).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération du rôle par nom: {e}")
            return None

    def get_all(self) -> List[Role]:
        try:
            return self.db_session.query(Role).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tous les rôles: {e}")
            return []

    def create(self, entity: Role) -> Role:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création du rôle: {e}")
            raise e

    def update(self, id: str, entity: Role) -> Optional[Role]:
        try:
            return None  # Les rôles sont généralement statiques
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour du rôle: {e}")
            raise e

    def delete(self, id: str) -> bool:
        try:
            return False # Les rôles ne sont pas supprimés
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la suppression du rôle: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[Role]:
        try:
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des rôles: {e}")
            return []
