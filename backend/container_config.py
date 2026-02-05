"""
Configuration du conteneur d'injection de dépendances.
"""
from sqlalchemy.orm import Session
from backend.core.dependency_container import container

# Interfaces
from backend.core.repository_interfaces import (
    IParcelRepository,
    IParcelHistoryRepository,
    IParcelReservationRepository,
    IVerificationLogRepository,
    IAlertRepository,
    IUserRepository,
    IRoleRepository,
    IAuditLogRepository,
    IMutationRepository,
    IDocumentRepository
)

# Repositories
from backend.infrastructure.repositories.parcel_repository import SqlParcelRepository
from backend.infrastructure.repositories.parcel_history_repository import SqlParcelHistoryRepository
from backend.infrastructure.repositories.parcel_reservation_repository import SqlParcelReservationRepository
from backend.infrastructure.repositories.verification_log_repository import SqlVerificationLogRepository
from backend.infrastructure.repositories.alert_repository import SqlAlertRepository
from backend.infrastructure.repositories.user_repository import SqlUserRepository
from backend.infrastructure.repositories.role_repository import SqlRoleRepository
from backend.infrastructure.repositories.audit_log_repository import SqlAuditLogRepository
from backend.infrastructure.repositories.mutation_repository import SqlMutationRepository
from backend.infrastructure.repositories.document_repository import SqlDocumentRepository

# Services
from backend.services.parcel_service import ParcelService
from backend.services.admin_service import AdminService
from backend.services.availability_service import AvailabilityService
from backend.services.alert_service import AlertService
from backend.services.email_service import EmailService, MockEmailService
from backend.services.audit_service import AuditService
from backend.services.auth_service import AuthService
from backend.services.search_service import SearchService
from backend.services.analytics_service import AnalyticsService
from backend.services.workflow_service import WorkflowService
from backend.services.document_service import DocumentService
from backend.services.mutation_service import MutationService

from backend.database import get_db

def configure_container():
    """Enregistre toutes les dépendances de l'application."""

    # Les sessions de DB sont gérées par `get_db` de FastAPI,
    # qui est injecté directement dans les constructeurs des repositories.
    # Le conteneur résoudra cela automatiquement.
    container.register_factory(Session, lambda: next(get_db()))

    # Repositories
    container.register_transient(IParcelRepository, SqlParcelRepository)
    container.register_transient(IParcelHistoryRepository, SqlParcelHistoryRepository)
    container.register_transient(IParcelReservationRepository, SqlParcelReservationRepository)
    container.register_transient(IVerificationLogRepository, SqlVerificationLogRepository)
    container.register_transient(IAlertRepository, SqlAlertRepository)
    container.register_transient(IUserRepository, SqlUserRepository)
    container.register_transient(IRoleRepository, SqlRoleRepository)
    container.register_transient(IAuditLogRepository, SqlAuditLogRepository)
    container.register_transient(IMutationRepository, SqlMutationRepository)
    container.register_transient(IDocumentRepository, SqlDocumentRepository)

    # Services
    container.register_transient(AdminService, AdminService)
    container.register_transient(AlertService, AlertService)
    container.register_transient(AvailabilityService, AvailabilityService)
    container.register_transient(ParcelService, ParcelService)
    container.register_transient(EmailService, MockEmailService)
    container.register_transient(AuditService, AuditService)
    container.register_transient(AuthService, AuthService)
    container.register_transient(SearchService, SearchService)
    container.register_transient(AnalyticsService, AnalyticsService)
    container.register_transient(WorkflowService, WorkflowService)
    container.register_transient(DocumentService, DocumentService)
    container.register_transient(MutationService, MutationService)

def get_parcel_service() -> ParcelService:
    """Fournisseur de dépendance pour ParcelService."""
    return container.resolve(ParcelService)

def get_admin_service() -> AdminService:
    """Fournisseur de dépendance pour AdminService."""
    return container.resolve(AdminService)

def get_availability_service() -> AvailabilityService:
    """Fournisseur de dépendance pour AvailabilityService."""
    return container.resolve(AvailabilityService)

def get_alert_service() -> AlertService:
    """Fournisseur de dépendance pour AlertService."""
    return container.resolve(AlertService)

def get_email_service() -> EmailService:
    """Fournisseur de dépendance pour EmailService."""
    return container.resolve(EmailService)

def get_audit_service() -> AuditService:
    """Fournisseur de dépendance pour AuditService."""
    return container.resolve(AuditService)

def get_auth_service() -> AuthService:
    """Fournisseur de dépendance pour AuthService."""
    return container.resolve(AuthService)

def get_search_service() -> SearchService:
    """Fournisseur de dépendance pour SearchService."""
    return container.resolve(SearchService)

def get_analytics_service() -> AnalyticsService:
    """Fournisseur de dépendance pour AnalyticsService."""
    return container.resolve(AnalyticsService)

def get_workflow_service() -> WorkflowService:
    """Fournisseur de dépendance pour WorkflowService."""
    return container.resolve(WorkflowService)

def get_document_service() -> DocumentService:
    """Fournisseur de dépendance pour DocumentService."""
    return container.resolve(DocumentService)

def get_mutation_service() -> MutationService:
    """Fournisseur de dépendance pour MutationService."""
    return container.resolve(MutationService)

