"""
SQLAlchemy Document model for file metadata (Story 6.1)
"""

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
from enum import Enum
from datetime import datetime
import uuid

Base = declarative_base()

class DocumentType(Enum):
    """Types of documents that can be associated with parcels"""
    TITLE_DEED = "title_deed"              # Titre de propriété
    SURVEY_PLAN = "survey_plan"            # Plan d'arpentage
    CONTRACT = "contract"                   # Contrat
    AUTHORIZATION = "authorization"         # Autorisation
    TECHNICAL_DOCUMENT = "technical_document"  # Document technique
    PHOTO = "photo"                        # Photographie
    TAX_DOCUMENT = "tax_document"          # Document fiscal
    OTHER = "other"                        # Autre type


class DocumentStatus(Enum):
    """Status of document validation"""
    EN_ATTENTE = "en_attente"              # Pending validation
    VALIDE = "valide"                      # Validated
    REFUSE = "refuse"                      # Rejected


class Document(Base):
    """
    SQLAlchemy Document model representing a file associated with a parcel

    Story 6.1: Gestion des documents liés aux parcelles

    Attributes:
        id: Unique identifier
        filename: Stored filename (UUID-based, secure)
        original_filename: User's original filename
        file_path: Full path to file on disk
        file_size: Size in bytes
        mime_type: MIME type (e.g., 'application/pdf')
        parcel_id: ID of associated parcel
        document_type: Type of document (enum)
        version: Version number (integer)
        is_public: Whether document is publicly accessible
        description: Optional description
        uploaded_by: ID of user who uploaded
        uploaded_at: Upload timestamp
    """
    __tablename__ = 'documents'

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # Using Integer as per database schema
    mime_type = Column(String, nullable=False)
    parcel_id = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    version = Column(Integer, default=1)
    is_public = Column(Integer, default=0)  # Using Integer as per database schema (SQLite doesn't have Boolean)
    deleted = Column(Integer, default=0)  # Using Integer as per database schema (0=False, 1=True)
    description = Column(Text)
    uploaded_by = Column(String, nullable=False)
    uploaded_at = Column(String, nullable=False)  # Using String as per database schema (TEXT in SQLite)

    def to_dict(self):
        """Convert document to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_formatted': self._format_file_size(self.file_size),
            'mime_type': self.mime_type,
            'parcel_id': self.parcel_id,
            'document_type': self.document_type,
            'version': self.version,
            'is_public': bool(self.is_public),  # Convert to boolean for API
            'deleted': bool(self.deleted),  # Convert to boolean for API
            'description': self.description or "",
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at
        }

    def _format_file_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes is None:
            return "0 B"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"