from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, Float, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User # Pour la relation 'created_by'

class Zone(Base):
    """
    Modèle SQLAlchemy représentant une zone urbaine ou géographique.
    """
    __tablename__ = 'zones'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    zone_type = Column(String, nullable=False, index=True) # Peut devenir un SQLEnum si les types sont fixes
    description = Column(Text)
    area = Column(Float)
    perimeter = Column(Float)
    geometry = Column(JSON)  # Stocke la géométrie au format GeoJSON
    regulations = Column(Text)
    allowed_uses = Column(JSON)  # JSON string
    restrictions = Column(JSON)  # JSON string
    
    created_by = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # --- Relations SQLAlchemy ---
    creator = relationship("User", foreign_keys=[created_by], backref="created_zones")
    # Une zone pourrait avoir plusieurs parcelles, cette relation serait dans le modèle Parcel
    # parcels = relationship("Parcel", back_populates="zone_obj")
    def to_dict(self):
        """Convertit l'objet Zone en dictionnaire."""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'zone_type': self.zone_type,
            'description': self.description,
            'area': self.area,
            'perimeter': self.perimeter,
            'geometry': self.geometry,
            'regulations': self.regulations,
            'allowed_uses': self.allowed_uses,
            'restrictions': self.restrictions,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
