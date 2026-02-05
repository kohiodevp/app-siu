from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User  # Pour les relations 'created_by', 'approved_by', 'rejected_by'
from .parcel import Parcel # Pour la relation 'parcel_id'

class Permit(Base):
    """
    Modèle SQLAlchemy représentant un permis.
    """
    __tablename__ = 'permits'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False, index=True)
    permit_type = Column(String, nullable=False) # Peut devenir un SQLEnum si les types sont fixes
    applicant_name = Column(String, nullable=False)
    applicant_contact = Column(Text)
    description = Column(Text)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default='pending', index=True) # Peut devenir un SQLEnum si les statuts sont fixes
    
    created_by = Column(String, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    approved_by = Column(String, ForeignKey('users.id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejected_by = Column(String, ForeignKey('users.id'), nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # --- Relations SQLAlchemy ---
    parcel = relationship("Parcel", backref="permits")
    creator = relationship("User", foreign_keys=[created_by], backref="created_permits")
    approver = relationship("User", foreign_keys=[approved_by], backref="approved_permits")
    rejecter = relationship("User", foreign_keys=[rejected_by], backref="rejected_permits")
    def to_dict(self):
        """Convertit l'objet Permit en dictionnaire."""
        return {
            'id': self.id,
            'parcel_id': self.parcel_id,
            'permit_type': self.permit_type,
            'applicant_name': self.applicant_name,
            'applicant_contact': self.applicant_contact,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejected_by': self.rejected_by,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'rejection_reason': self.rejection_reason
        }
