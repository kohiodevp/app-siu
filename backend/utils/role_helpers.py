"""
Helpers pour la gestion des rôles utilisateur
"""
from typing import Union
from backend.models.user import User, UserRole, Role


def get_role_value(role: Union[str, Role, UserRole, None]) -> str:
    """
    Normalise un rôle vers sa valeur string
    
    Args:
        role: Rôle sous n'importe quelle forme
        
    Returns:
        str: Valeur normalisée du rôle (lowercase)
    """
    if role is None:
        return "citizen"  # Rôle par défaut
    
    if isinstance(role, str):
        return role.lower()
    
    if isinstance(role, UserRole):
        return role.value.lower()
    
    if isinstance(role, Role):
        return role.name.lower()
    
    # Fallback - essayer d'extraire l'attribut
    if hasattr(role, 'value'):
        return str(role.value).lower()
    elif hasattr(role, 'name'):
        return str(role.name).lower()
    
    return str(role).lower()


def is_admin(user: User) -> bool:
    """
    Vérifie si un utilisateur est administrateur
    
    Args:
        user: Utilisateur à vérifier
        
    Returns:
        bool: True si admin
    """
    role_value = get_role_value(user.role)
    return role_value == 'administrator'


def is_admin_or_manager(user: User) -> bool:
    """
    Vérifie si un utilisateur est admin ou manager
    
    Args:
        user: Utilisateur à vérifier
        
    Returns:
        bool: True si admin ou manager
    """
    role_value = get_role_value(user.role)
    return role_value in ['administrator', 'manager']


def has_role(user: User, *roles: str) -> bool:
    """
    Vérifie si un utilisateur a un des rôles spécifiés
    
    Args:
        user: Utilisateur à vérifier
        roles: Liste de rôles à vérifier
        
    Returns:
        bool: True si l'utilisateur a un des rôles
    """
    user_role = get_role_value(user.role)
    normalized_roles = [r.lower() for r in roles]
    return user_role in normalized_roles
