from datetime import datetime
from enum import Enum as PyEnum
import uuid
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from ..database import Base
from .user import User  # Pour la relation 'uploaded_by'
from .parcel import Parcel # Pour la relation 'parcel_id'

class DocumentType(PyEnum):
    """Types de documents pouvant être associés aux parcelles"""
    TITLE_DEED = "title_deed"              # Titre de propriété
    SURVEY_PLAN = "survey_plan"            # Plan d'arpentage
    CONTRACT = "contract"                   # Contrat
    AUTHORIZATION = "authorization"         # Autorisation
    TECHNICAL_DOCUMENT = "technical_document"  # Document technique
    PHOTO = "photo"                        # Photographie
    TAX_DOCUMENT = "tax_document"          # Document fiscal
    OTHER = "other"                        # Autre type

class Document(Base):
    """
    Modèle SQLAlchemy représentant un fichier associé à une parcelle.
    """
    __tablename__ = 'documents'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False, index=True)
    document_type = Column(SQLEnum(DocumentType, name='document_type'), nullable=False)
    version = Column(Integer, default=1)
    is_public = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False) # Présent dans la DDL originale
    description = Column(String)
    
    uploaded_by = Column(String, ForeignKey('users.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now, nullable=False)

    # --- Logic methods ---

    def to_dict(self):
        """Convertit l'objet Document en dictionnaire."""
        # Formater la taille du fichier pour l'affichage
        file_size_formatted = self._format_file_size(self.file_size)
        
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_formatted': file_size_formatted,
            'mime_type': self.mime_type,
            'parcel_id': self.parcel_id,
            'document_type': self.document_type.value if hasattr(self.document_type, 'value') else self.document_type,
            'version': self.version,
            'is_public': self.is_public,
            'deleted': self.deleted,
            'description': self.description,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Formate la taille du fichier en unités lisibles"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    # --- Relations SQLAlchemy ---
    parcel = relationship("Parcel", backref="documents")
    uploader = relationship("User", foreign_keys=[uploaded_by], backref="uploaded_documents")