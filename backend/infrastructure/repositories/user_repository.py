"""
Implémentation du repository pour les utilisateurs.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc as sql_exceptions
from backend.core.repository_interfaces import IUserRepository
from backend.models.user import User
from backend.utils.db_helpers import safe_ilike


class SqlUserRepository(IUserRepository):
    """
    Implémentation SQLAlchemy du repository des utilisateurs.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[User]:
        try:
            return self.db_session.query(User)\
                .options(joinedload(User.role))\
                .filter(User.id == id)\
                .first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'utilisateur par ID: {e}")
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return self.db_session.query(User).filter(User.email == email).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'utilisateur par email: {e}")
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            return self.db_session.query(User)\
                .options(joinedload(User.role))\
                .filter(User.username == username)\
                .first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'utilisateur par nom d'utilisateur: {e}")
            return None

    def get_all(self) -> List[User]:
        try:
            return self.db_session.query(User).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tous les utilisateurs: {e}")
            return []

    def create(self, entity: User) -> User:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.IntegrityError as e:
            self.db_session.rollback()
            raise e
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création de l'utilisateur: {e}")
            raise e

    def update(self, id: str, entity: User) -> Optional[User]:
        try:
            existing = self.get_by_id(id)
            if existing:
                existing.username = entity.username
                existing.email = entity.email
                existing.first_name = entity.first_name
                existing.last_name = entity.last_name
                existing.role = entity.role
                existing.is_active = entity.is_active
                return existing
            return None
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la mise à jour de l'utilisateur: {e}")
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
            print(f"Erreur lors de la suppression de l'utilisateur: {e}")
            return False

    def search(self, criteria: Dict[str, Any]) -> List[User]:
        try:
            query = self.db_session.query(User)
            if "username" in criteria:
                query = query.filter(safe_ilike(User.username, criteria['username']))
            if "email" in criteria:
                query = query.filter(safe_ilike(User.email, criteria['email']))
            if "role" in criteria:
                # Handle role comparison properly - could be role name or role ID
                role_param = criteria["role"]
                if isinstance(role_param, str):
                    # If it's a string, compare with role name
                    from backend.models.user import Role
                    query = query.join(User.role).filter(Role.name == role_param)
                else:
                    # If it's an object, compare directly
                    query = query.filter(User.role == role_param)
            return query.all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des utilisateurs: {e}")
            return []
