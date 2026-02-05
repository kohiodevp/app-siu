"""
Configuration de l'application
"""
import os
from typing import Optional


class Config:
    """
    Classe de configuration centralisée
    """
    
    # Base de données
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./siu_database.db')
    DATABASE_POOL_SIZE: int = int(os.getenv('DATABASE_POOL_SIZE', '5'))
    DATABASE_POOL_TIMEOUT: int = int(os.getenv('DATABASE_POOL_TIMEOUT', '30'))
    
    # JWT
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    # WebSocket
    WEBSOCKET_HOST: str = os.getenv('WEBSOCKET_HOST', 'localhost')
    WEBSOCKET_PORT: int = int(os.getenv('WEBSOCKET_PORT', '8000'))
    
    # Divers
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'SIU Land Registry System')
    VERSION: str = os.getenv('VERSION', '1.0.0')
    
    @classmethod
    def validate(cls) -> None:
        """
        Valide que la configuration est correcte
        """
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            print("AVERTISSEMENT: Clé secrète par défaut utilisée. Changer pour la production!")
        
        if cls.DEBUG:
            print("AVERTISSEMENT: Mode debug activé")