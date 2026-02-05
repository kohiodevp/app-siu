from datetime import datetime
from enum import Enum as PyEnum
import uuid
import bcrypt
from sqlalchemy import (
    Column, String, Boolean, DateTime, Integer, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from ..database import Base

class UserRole(PyEnum):
    """Enumération des rôles utilisateur dans le système SIU.
    Utilisé pour la logique métier et les valeurs par défaut."""
    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    OFFICER = "officer"
    CITIZEN = "citizen"
    CONSULTANT = "consultant"

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    users = relationship("User", back_populates="role")

class User(Base):
    """
    Modèle SQLAlchemy représentant un utilisateur du système SIU.
    """
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs):
        # Assigner le mot de passe s'il est présent, pour le hacher
        if 'password' in kwargs:
            password = kwargs.pop('password')
            self.set_password(password)
        
        # S'assurer qu'un rôle par défaut est assigné si non fourni
        # Note : ceci ne fonctionne que pour la création d'objets, pas pour la lecture depuis la BDD
        # La logique de rôle doit être gérée au niveau du service/contrôleur
        
        super().__init__(*args, **kwargs)

    def set_password(self, password: str):
        """Hash et définit le mot de passe."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire (sans le mot de passe)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.name if self.role else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
