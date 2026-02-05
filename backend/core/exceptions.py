"""
Exceptions personnalisées pour l'application
"""
from typing import Optional


class SIUException(Exception):
    """
    Exception de base pour l'application SIU
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class EntityNotFoundException(SIUException):
    """
    Levée quand une entité n'est pas trouvée
    """
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(
            f"{entity_type} avec l'ID {entity_id} n'a pas été trouvé(e)",
            error_code="ENTITY_NOT_FOUND"
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class InvalidDataException(SIUException):
    """
    Levée quand les données fournies sont invalides
    """
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, error_code="INVALID_DATA")
        self.field = field


class UnauthorizedException(SIUException):
    """
    Levée quand l'accès à une ressource est non autorisé
    """
    def __init__(self, message: str = "Accès non autorisé"):
        super().__init__(message, error_code="UNAUTHORIZED")


class InsufficientPermissionsException(SIUException):
    """
    Levée quand les permissions sont insuffisantes
    """
    def __init__(self, required_permission: str):
        super().__init__(
            f"Permissions insuffisantes. Permission requise: {required_permission}",
            error_code="INSUFFICIENT_PERMISSIONS"
        )
        self.required_permission = required_permission


class BusinessRuleViolationException(SIUException):
    """
    Levée quand une règle métier est violée
    """
    def __init__(self, rule: str, details: Optional[str] = None):
        message = f"Violation de règle métier: {rule}"
        if details:
            message += f" - Détails: {details}"
        
        super().__init__(message, error_code="BUSINESS_RULE_VIOLATION")
        self.rule = rule
        self.details = details