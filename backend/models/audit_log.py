from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from .user import User # Importer pour la relation User
from .parcel import Parcel # Importer pour la relation Parcel

# Ces classes peuvent être converties en enum.Enum pour une meilleure typage
# et cohérence, mais nous les gardons comme des classes simples pour ne pas
# casser le code existant si elles sont utilisées directement ailleurs.
class AuditActionType:
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    VALIDATE = "validate"
    ASSIGN = "assign"


class AuditEntityType:
    USER = "user"
    PARCEL = "parcel"
    DOCUMENT = "document"
    OWNER = "owner"
    ALERT = "alert"
    SYSTEM = "system"


class AuditStatus:
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    
    action = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(String, nullable=True, index=True)
    
    # user_id doit être de type String car User.id est un String
    user_id = Column(String, ForeignKey('users.id'), nullable=True, index=True)
    username = Column(String, nullable=True)
    user_role = Column(String, nullable=True)
    
    user_ip = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    request_method = Column(String, nullable=True)
    request_path = Column(String, nullable=True)
    
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    changes = Column(JSON, nullable=True)
    
    # Utiliser datetime.now pour une meilleure gestion des fuseaux horaires par défaut
    timestamp = Column(DateTime, default=datetime.now, nullable=False, index=True)
    duration_ms = Column(Integer, nullable=True)
    status = Column(String, default=AuditStatus.SUCCESS, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    
    response_status = Column(Integer, nullable=True)
    response_size = Column(BigInteger, nullable=True)
    
    is_sensitive = Column(Boolean, default=False)
    requires_review = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, nullable=True)
    # reviewed_by doit être de type String car User.id est un String
    reviewed_by = Column(String, ForeignKey('users.id'), nullable=True)
    
    metadata_ext = Column(JSON, nullable=True)

    # Relations SQLAlchemy
    user = relationship("User", foreign_keys=[user_id], backref="audit_logs_created")
    reviewer = relationship("User", foreign_keys=[reviewed_by], backref="audit_logs_reviewed")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', entity='{self.entity_type}:{self.entity_id}', user={self.user_id})>"
    
    # `to_dict` et `create_audit` peuvent être conservées si elles sont utilisées
    # mais souvent redondantes avec Pydantic et l'ORM.
    # Pour l'instant, je les laisse mais les futures refactorisations pourraient les supprimer.
    def to_dict(self):
        result = {
            'id': self.id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'user_id': self.user_id,
            'username': self.username,
            'user_role': self.user_role,
            'user_ip': self.user_ip,
            'request_method': self.request_method,
            'request_path': self.request_path,
            'old_data': self.old_data,
            'new_data': self.new_data,
            'changes': self.changes,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'duration_ms': self.duration_ms,
            'status': self.status,
            'error_message': self.error_message,
            'response_status': self.response_status,
            'is_sensitive': self.is_sensitive,
            'requires_review': self.requires_review,
            'reviewed': self.reviewed,
            'metadata': self.metadata_ext
        }
        if self.is_sensitive:
            result.pop('user_ip', None)
            result.pop('user_agent', None)
            result.pop('old_data', None)
            result.pop('new_data', None)
            result.pop('changes', None)
            result.pop('error_message', None)
        return result
    
    @property
    def action_label(self):
        labels = {
            'create': 'Création', 'read': 'Consultation', 'update': 'Modification', 'delete': 'Suppression',
            'login': 'Connexion', 'logout': 'Déconnexion', 'export': 'Export', 'import': 'Import',
            'upload': 'Upload', 'download': 'Téléchargement', 'validate': 'Validation', 'assign': 'Attribution'
        }
        return labels.get(self.action, self.action)
    
    @property
    def entity_label(self):
        labels = {
            'user': 'Utilisateur', 'parcel': 'Parcelle', 'document': 'Document', 'owner': 'Propriétaire',
            'alert': 'Alerte', 'system': 'Système'
        }
        return labels.get(self.entity_type, self.entity_type)
    
    @property
    def has_changes(self):
        return bool(self.changes and len(self.changes) > 0)
    
    @classmethod
    def create_audit(
        cls, action: str, entity_type: str, entity_id: str = None, user_id: str = None, # user_id est maintenant String
        username: str = None, user_role: str = None, old_data: dict = None, new_data: dict = None,
        changes: dict = None, user_ip: str = None, user_agent: str = None, request_method: str = None,
        request_path: str = None, duration_ms: int = None, status: str = AuditStatus.SUCCESS,
        error_message: str = None, response_status: int = None, is_sensitive: bool = False, metadata: dict = None
    ):
        return cls(
            action=action, entity_type=entity_type, entity_id=entity_id, user_id=user_id,
            username=username, user_role=user_role, old_data=old_data, new_data=new_data,
            changes=changes, user_ip=user_ip, user_agent=user_agent, request_method=request_method,
            request_path=request_path, duration_ms=duration_ms, status=status,
            error_message=error_message, response_status=response_status, is_sensitive=is_sensitive,
            metadata_ext=metadata
        )


class ParcelHistory(Base):
    __tablename__ = 'parcel_history'

    id = Column(Integer, primary_key=True, autoincrement=True) # ID auto-incrémenté
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False, index=True)
    action = Column(String, nullable=False)
    field = Column(String, nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False, index=True) # Utiliser datetime.now
    updated_by = Column(String, ForeignKey('users.id'), nullable=True) # updated_by doit être String

    # Relations SQLAlchemy
    parcel = relationship("Parcel", backref="history_logs")
    updater = relationship("User", foreign_keys=[updated_by], backref="parcel_history_updates")

    def to_dict(self):
        return {
            'id': self.id,
            'parcel_id': self.parcel_id,
            'action': self.action,
            'field': self.field,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'updated_by': self.updated_by
        }