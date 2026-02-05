"""
Helpers pour la gestion de base de données
"""
from sqlalchemy import text


def escape_like_pattern(pattern: str) -> str:
    """
    Échappe les caractères spéciaux dans les patterns LIKE/ILIKE
    pour éviter les injections SQL
    
    Args:
        pattern: Pattern à échapper
        
    Returns:
        str: Pattern échappé
    """
    if not pattern:
        return pattern
    
    # Échapper les caractères spéciaux de SQL LIKE
    pattern = pattern.replace('\\', '\\\\')  # Backslash d'abord
    pattern = pattern.replace('%', r'\%')
    pattern = pattern.replace('_', r'\_')
    
    return pattern


def safe_ilike(column, search_term: str):
    """
    Crée un filtre ILIKE sécurisé avec échappement
    
    Args:
        column: Colonne SQLAlchemy
        search_term: Terme de recherche
        
    Returns:
        Filtre SQLAlchemy sécurisé
    """
    escaped_term = escape_like_pattern(search_term)
    return column.ilike(f"%{escaped_term}%", escape='\\')
