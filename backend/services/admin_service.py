from typing import Dict, Any, Optional, List
from sqlalchemy.exc import IntegrityError # Import IntegrityError for exception handling

from backend.models.user import User, UserRole
from backend.core.repository_interfaces import IUserRepository, IRoleRepository
from backend.services.email_service import EmailService # Import the interface

class AdminService:
    """
    Service pour la gestion des utilisateurs par les administrateurs, avec persistance en base de données.
    """
    
    def __init__(self, user_repository: IUserRepository, role_repository: IRoleRepository, email_service: EmailService):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.email_service = email_service
        
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        Crée un nouvel utilisateur en base de données.
        """
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        role_input = user_data.get('role', UserRole.CITIZEN.value)
        
        role_obj = self.role_repository.get_by_name(role_input.lower())
        if not role_obj:
            raise ValueError(f"Rôle invalide: {role_input}")

        new_user = User(
            username=username,
            email=email,
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role=role_obj
        )
        new_user.set_password(password)

        try:
            created_user = self.user_repository.create(new_user)
            
            confirmation_message = f"Veuillez confirmer votre inscription et vos identifiants."
            self.email_service.send_confirmation_email(created_user.email, created_user.username, confirmation_message)
            
            return created_user

        except IntegrityError:
            raise ValueError(f"Un utilisateur existe déjà avec ce nom d'utilisateur ou cette adresse email")
        
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID."""
        return self.user_repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Récupère un utilisateur par son nom d'utilisateur."""
        return self.user_repository.get_by_username(username)
        
    def update_user_password(self, user_id: str, new_password: str) -> bool:
        """Met à jour le mot de passe d'un utilisateur."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        user.set_password(new_password)
        updated_user = self.user_repository.update(user_id, user)
        return updated_user is not None

    def get_all_users(self) -> List[User]:
        """Récupère tous les utilisateurs."""
        return self.user_repository.get_all()

    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Met à jour les informations d'un utilisateur."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        if not kwargs:
            return user

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        updated_user = self.user_repository.update(user_id, user)
        return updated_user

    def assign_role_to_user(self, user_id: str, role_name: str) -> bool:
        """Attribue un rôle à un utilisateur."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False

        role = self.role_repository.get_by_name(role_name.lower())
        if not role:
            raise ValueError(f"Le rôle '{role_name}' n'existe pas.")

        user.role = role
        updated_user = self.user_repository.update(user_id, user)
        return updated_user is not None