from datetime import datetime
from enum import Enum as PyEnum
import uuid
from sqlalchemy import (
    Column, String, Float, Text, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User  # Pour les relations 'initiated_by_user_id' et 'approved_by_user_id'
from .parcel import Parcel # Pour la relation 'parcel_id'

class MutationType(PyEnum):
    """Types de mutations de parcelles"""
    SALE = "sale"  # Vente
    DONATION = "donation"  # Donation
    INHERITANCE = "inheritance"  # Héritage
    EXCHANGE = "exchange"  # Échange
    EXPROPRIATION = "expropriation"  # Expropriation
    SUBDIVISION = "subdivision"  # Subdivision
    MERGE = "merge"  # Fusion
    OTHER = "other"  # Autre

class MutationStatus(PyEnum):
    """Statuts d'une mutation"""
    PENDING = "pending"  # En attente
    APPROVED = "approved"  # Approuvée
    REJECTED = "rejected"  # Rejetée
    COMPLETED = "completed"  # Complétée
    CANCELLED = "cancelled"  # Annulée

class ParcelMutation(Base):
    """
    Modèle SQLAlchemy représentant une mutation (transfert) de parcelle.
    """
    __tablename__ = 'parcel_mutations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False, index=True)
    mutation_type = Column(SQLEnum(MutationType, name='mutation_type'), nullable=False)
    
    # from_owner_id et to_owner_id réfèrent à une table 'owners' qui n'est pas un modèle SQLAlchemy ici.
    # Dans la migration, ces champs sont INTEGER, mais ici nous les mettons en STRING
    # par cohérence avec les IDs d'utilisateurs. Cela nécessitera une clarification architecturale.
    from_owner_id = Column(String, nullable=True) # Pas de ForeignKey directe pour l'instant
    to_owner_id = Column(String, nullable=True)   # Pas de ForeignKey directe pour l'instant
    
    initiated_by_user_id = Column(String, ForeignKey('users.id'), nullable=False)
    price = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(SQLEnum(MutationStatus, name='mutation_status'), nullable=False, default=MutationStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    approved_by_user_id = Column(String, ForeignKey('users.id'), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # --- Relations SQLAlchemy ---
    parcel = relationship("Parcel", backref="mutations")
    initiator = relationship("User", foreign_keys=[initiated_by_user_id], backref="initiated_mutations")
    approver = relationship("User", foreign_keys=[approved_by_user_id], backref="approved_mutations")

    # --- Logic methods ---

    def to_dict(self):
        """Convertit l'objet ParcelMutation en dictionnaire."""
        return {
            'id': self.id,
            'parcel_id': self.parcel_id,
            'mutation_type': self.mutation_type.value if hasattr(self.mutation_type, 'value') else self.mutation_type,
            'from_owner_id': self.from_owner_id,
            'to_owner_id': self.to_owner_id,
            'initiated_by_user_id': self.initiated_by_user_id,
            'price': self.price,
            'notes': self.notes,
            'status': self.status.value if hasattr(self.status, 'value') else self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'approved_by_user_id': self.approved_by_user_id,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'rejection_reason': self.rejection_reason
        }

    def approve(self, user_id):
        """Approuve la mutation."""
        self.status = MutationStatus.APPROVED
        self.approved_at = datetime.now()
        self.approved_by_user_id = user_id
        self.updated_at = datetime.now()

    def reject(self, user_id, reason):
        """Rejette la mutation."""
        self.status = MutationStatus.REJECTED
        self.approved_by_user_id = user_id
        self.rejection_reason = reason
        self.updated_at = datetime.now()

    def complete(self):
        """Marque la mutation comme complétée."""
        self.status = MutationStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def cancel(self):
        """Annule la mutation."""
        self.status = MutationStatus.CANCELLED
        self.updated_at = datetime.now()

    # Relations potentielles pour from_owner_id et to_owner_id si un modèle Owner est créé
    # from_owner = relationship("Owner", foreign_keys=[from_owner_id])
    # to_owner = relationship("Owner", foreign_keys=[to_owner_id])