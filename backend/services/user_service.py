from datetime import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, or_ # Import func and or_ for queries

from backend.models.user import User, Role # Import Role model
# from backend.database import get_db_connection # Not needed anymore

class UserService:
    """
    Service pour la gestion des actions utilisateur en libre-service.
    Ex: mise à jour de son propre profil.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID depuis la base de données."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Récupère un utilisateur par son nom d'utilisateur depuis la base de données."""
        return self.db.query(User).filter(User.username == username).first()


    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Optional[User]:
        """
        Met à jour le profil d'un utilisateur (ex: nom, prénom).
        Ne permet pas de changer le rôle ou le nom d'utilisateur.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in profile_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user) # Refresh to get the updated_at from DB
        return user

    def get_role_statistics(self) -> Dict[str, Any]:
        """
        Récupère les statistiques des rôles utilisateurs.
        
        Returns:
            Statistiques par rôle (nombre d'utilisateurs, pourcentage, etc.)
        """
        # Count users per role
        role_counts = self.db.query(
            Role.name.label('role'),
            func.count(User.id).label('count')
        ).outerjoin(User).group_by(Role.id, Role.name).all()
        
        # Total users
        total_users = self.db.query(func.count(User.id)).scalar()
        
        # Build statistics
        stats = {
            'total_users': total_users,
            'roles': []
        }
        
        for role_name, count in role_counts:
            percentage = (count / total_users * 100) if total_users > 0 else 0
            stats['roles'].append({
                'name': role_name,
                'count': count,
                'percentage': round(percentage, 2)
            })
        
        return stats


    def update_user_role(self, user_id: str, role_name: str, updated_by: str) -> Optional[User]:
        """
        Met à jour le rôle d'un utilisateur.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        role = self.db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise ValueError(f"Role '{role_name}' not found")

        user.role = role
        self.db.commit()
        self.db.refresh(user)

        # Enregistrer dans l'audit log (assuming AuditService is also refactored to use db session)
        # NOTE: AuditService also needs to be refactored to accept a db session
        # and handle its own ORM interactions. For now, we'll keep the import,
        # but the instantiation needs a db session.
        from backend.services.audit_service import AuditService
        audit_service = AuditService() # This will need to change when AuditService is refactored
        audit_service.log_action(
            user_id=updated_by,
            action="update_user_role",
            entity_type="user",
            entity_id=user_id,
            details={"new_role": role_name}
        )

        return user

    def get_permissions_for_role(self, role_name: str) -> List[str]:
        """
        Récupère les permissions associées à un rôle.
        """
        # Définir les permissions par rôle en utilisant l'énumération UserRole
        permissions_map = {
            UserRole.ADMINISTRATOR.value: [ # Use .value
                'user.create', 'user.read', 'user.update', 'user.delete',
                'parcel.create', 'parcel.read', 'parcel.update', 'parcel.delete',
                'document.create', 'document.read', 'document.update', 'document.delete',
                'report.create', 'report.read', 'report.export',
                'audit.read', 'system.configure'
            ],
            UserRole.MANAGER.value: [ # Use .value
                'user.read',
                'parcel.create', 'parcel.read', 'parcel.update',
                'document.create', 'document.read', 'document.update',
                'report.create', 'report.read', 'report.export'
            ],
            UserRole.OFFICER.value: [ # Use .value
                'parcel.read', 'parcel.update',
                'document.read', 'document.create',
                'report.read'
            ],
            UserRole.CITIZEN.value: [ # Use .value
                'parcel.read',
                'document.read'
            ],
            UserRole.CONSULTANT.value: [ # Use .value
                'parcel.read',
                'document.read',
                'report.read', 'report.export'
            ]
        }

        return permissions_map.get(role_name, [])

    def get_users_with_filters(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """
        Récupère les utilisateurs avec pagination et filtres.
        """
        query = self.db.query(User).join(Role)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern)
                )
            )

        if role:
            query = query.filter(Role.name == role)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # Add sorting
        valid_sort_fields = {
            "id": User.id, 
            "username": User.username, 
            "email": User.email, 
            "first_name": User.first_name, 
            "last_name": User.last_name, 
            "created_at": User.created_at, 
            "updated_at": User.updated_at, 
            "is_active": User.is_active,
            "role": Role.name # Allow sorting by role name
        }
        sort_column = valid_sort_fields.get(sort_by, User.created_at)
        
        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Add pagination
        users = query.offset(skip).limit(limit).all()

        return users

    def count_users_with_filters(
        self,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """
        Compte le nombre total d'utilisateurs correspondant aux filtres.
        """
        query = self.db.query(User).join(Role)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern)
                )
            )

        if role:
            query = query.filter(Role.name == role)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        return query.count()


    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change le mot de passe d'un utilisateur après avoir vérifié l'ancien mot de passe.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        if not user.verify_password(current_password):
            return False

        user.set_password(new_password) # Use the method on the SQLAlchemy model
        self.db.commit()
        self.db.refresh(user)
        return True
