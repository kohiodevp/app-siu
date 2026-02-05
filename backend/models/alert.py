from datetime import datetime
from enum import Enum as PyEnum
import uuid
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User  # Pour la relation 'triggered_by' et 'acknowledged_by'
from .parcel import Parcel # Pour la relation 'parcel_id'

class AlertType(PyEnum):
    """Types d'alertes dans le système"""
    DOUBLE_ATTRIBUTION_ATTEMPT = "double_attribution_attempt"
    CONFLICT_DETECTED = "conflict_detected"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RESERVATION_EXPIRED = "reservation_expired"

class AlertSeverity(PyEnum):
    """Niveaux de sévérité des alertes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Alert(Base):
    """
    Modèle SQLAlchemy pour les alertes système et la prévention de la fraude.
    """
    __tablename__ = 'alerts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_type = Column(SQLEnum(AlertType, name='alert_type'), nullable=False)
    severity = Column(SQLEnum(AlertSeverity, name='alert_severity'), nullable=False)
    
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=True, index=True)
    triggered_by = Column(String, ForeignKey('users.id'), nullable=True)
    message = Column(Text, nullable=False) # Utiliser Text pour messages potentiellement longs
    
    created_at = Column(DateTime, default=datetime.now, nullable=False, index=True)
    acknowledged = Column(Boolean, default=False, index=True)
    acknowledged_by = Column(String, ForeignKey('users.id'), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

    # --- Logic methods ---

    def to_dict(self):
        """Convertit l'objet Alert en dictionnaire."""
        return {
            'id': self.id,
            'alert_type': self.alert_type.value if hasattr(self.alert_type, 'value') else self.alert_type,
            'severity': self.severity.value if hasattr(self.severity, 'value') else self.severity,
            'parcel_id': self.parcel_id,
            'triggered_by': self.triggered_by,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'acknowledged': self.acknowledged,
            'acknowledged_by': self.acknowledged_by,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }

    def acknowledge(self, user_id):
        """Marque l'alerte comme acquittée."""
        self.acknowledged = True
        self.acknowledged_by = user_id
        self.acknowledged_at = datetime.now()

    @staticmethod
    def _from_db_row(row):
        """Compatibilité avec l'ancien code. Crée une alerte à partir d'une ligne de DB."""
        # Note: c'est une solution temporaire pour la migration.
        # Idéalement, on utilise uniquement les objets SQLAlchemy.
        from backend.models.alert import Alert, AlertType, AlertSeverity
        alert = Alert()
        alert.id = row['id']
        alert.alert_type = AlertType(row['alert_type']) if isinstance(row['alert_type'], str) else row['alert_type']
        alert.severity = AlertSeverity(row['severity']) if isinstance(row['severity'], str) else row['severity']
        alert.parcel_id = row['parcel_id']
        alert.triggered_by = row['triggered_by']
        alert.message = row['message']
        alert.created_at = datetime.fromisoformat(row['created_at']) if isinstance(row['created_at'], str) else row['created_at']
        alert.acknowledged = bool(row['acknowledged'])
        alert.acknowledged_by = row['acknowledged_by']
        alert.acknowledged_at = datetime.fromisoformat(row['acknowledged_at']) if isinstance(row['acknowledged_at'], str) else row['acknowledged_at']
        return alert

    # --- Relations SQLAlchemy ---
    parcel = relationship("Parcel", backref="alerts")
    triggerer = relationship("User", foreign_keys=[triggered_by], backref="triggered_alerts")
    acknowledger = relationship("User", foreign_keys=[acknowledged_by], backref="acknowledged_alerts")