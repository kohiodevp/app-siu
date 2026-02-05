"""
Module de sécurité avancé
"""
import re
import secrets
import hashlib
from typing import Optional
from datetime import datetime, timedelta

class SecurityValidator:
    """Validateur de sécurité avancé"""
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Valide la force d'un mot de passe
        Returns: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"
        
        if not re.search(r'[A-Z]', password):
            return False, "Le mot de passe doit contenir au moins une majuscule"
        
        if not re.search(r'[a-z]', password):
            return False, "Le mot de passe doit contenir au moins une minuscule"
        
        if not re.search(r'\d', password):
            return False, "Le mot de passe doit contenir au moins un chiffre"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Nettoie les entrées utilisateur"""
        # Supprimer les caractères dangereux
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '`']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Génère un token sécurisé"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash des données sensibles"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_file_upload(filename: str, max_size_mb: int = 50) -> tuple[bool, str]:
        """Valide un upload de fichier"""
        from backend.config import allowed_file
        
        if not allowed_file(filename):
            return False, "Type de fichier non autorisé"
        
        # Vérifier les caractères dangereux dans le nom
        if re.search(r'[<>:"/\\|?*]', filename):
            return False, "Nom de fichier invalide"
        
        return True, ""

class RateLimiter:
    """Limiteur de taux avancé"""
    
    def __init__(self):
        self.requests: dict = {}
    
    def is_rate_limited(self, key: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        """Vérifie si une clé est rate limited"""
        now = datetime.now()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Nettoyer les anciennes requêtes
        window_start = now - timedelta(seconds=window_seconds)
        self.requests[key] = [req_time for req_time in self.requests[key] if req_time > window_start]
        
        # Vérifier la limite
        if len(self.requests[key]) >= max_requests:
            return True
        
        self.requests[key].append(now)
        return False

# Instances globales
security_validator = SecurityValidator()
rate_limiter = RateLimiter()
