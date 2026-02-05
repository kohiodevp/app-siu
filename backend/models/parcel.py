from datetime import datetime
from enum import Enum
import uuid
from sqlalchemy import (
    Column, String, Float, Text, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User  # Importer pour la relation

# Les Enums et classes de catégories peuvent être conservées car elles
# représentent la logique métier, indépendamment de la persistance.
class ParcelCategory(Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    # ... (garder toutes les catégories de l'ancien fichier)
    INDEFINI = "Indefini"

class Parcel(Base):
    """
    Modèle SQLAlchemy représentant une parcelle foncière.
    """
    __tablename__ = 'parcels'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reference_cadastrale = Column(String, unique=True, nullable=False, index=True)
    
    # Coordonnées stockées séparément comme dans le schéma de la BDD
    coordinates_lat = Column(Float, nullable=False)
    coordinates_lng = Column(Float, nullable=False)
    
    area = Column(Float, nullable=False)
    address = Column(Text, nullable=False)
    category = Column(String, nullable=False, index=True, default=ParcelCategory.INDEFINI.value)
    description = Column(Text)
    
    # Utiliser le type JSON natif si la BDD le supporte (SQLite le supporte)
    geometry = Column(JSON) 
    
    owner_id = Column(String, ForeignKey('users.id'), index=True)
    created_by = Column(String, ForeignKey('users.id'))
    
    cadastral_plan_ref = Column(String)
    status = Column(String, default='available')
    zone = Column(String, index=True)
    region = Column(String)
    province = Column(String)
    localite = Column(String)
    
    # Nouveaux champs potentiels basés sur l'ancien create_table
    realeve = Column(String)
    reaplanurb = Column(String)
    reaimplant = Column(String)
    command = Column(String)
    numsection = Column(String)
    numlot = Column(String)
    numparc = Column(String)
    commune = Column(String)
    anneeachev = Column(String)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # --- Relations SQLAlchemy ---
    owner = relationship("User", foreign_keys=[owner_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    # La relation vers l'historique, les documents, etc. sera ajoutée
    # lorsque ces modèles seront aussi convertis.
    # history = relationship("ParcelHistory", back_populates="parcel")
    # documents = relationship("Document", back_populates="parcel")

    # --- Logic methods ---

    def to_dict(self):
        """Convertit l'objet Parcel en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'reference_cadastrale': self.reference_cadastrale,
            'coordinates': {
                'lat': self.coordinates_lat,
                'lng': self.coordinates_lng
            },
            'area': self.area,
            'address': self.address,
            'category': self.category,
            'description': self.description,
            'geometry': self.geometry,
            'owner_id': self.owner_id,
            'created_by': self.created_by,
            'cadastral_plan_ref': self.cadastral_plan_ref,
            'status': self.status,
            'zone': self.zone,
            'region': self.region,
            'province': self.province,
            'localite': self.localite,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def update_info(self, **kwargs):
        """Met à jour les informations de la parcelle."""
        updated_by = kwargs.pop('updated_by', None)
        
        # Handle coordinates special case
        if 'coordinates' in kwargs:
            coords = kwargs.pop('coordinates')
            if isinstance(coords, dict):
                self.coordinates_lat = coords.get('lat', self.coordinates_lat)
                self.coordinates_lng = coords.get('lng', self.coordinates_lng)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
