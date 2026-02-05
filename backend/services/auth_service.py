from datetime import datetime, timedelta
from backend.models.user import User
from backend.services.admin_service import AdminService
from typing import Dict, Any, Optional
import secrets
from jose import JWTError, jwt
import re

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    import warnings
    warnings.warn(
        "SECRET_KEY non définie dans les variables d'environnement. "
        "Veuillez définir la variable SECRET_KEY pour des raisons de sécurité. "
        "Utilisation d'une clé temporaire pour le développement uniquement.",
        UserWarning
    )
    SECRET_KEY = "dev-temporary-secret-key-change-in-production"  # Only for development
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 heure pour des raisons de sécurité (était 24 heures)

class AuthService:
    """
    Service pour l'authentification des utilisateurs

    Correspond à la FR2: Utilisateurs peuvent s'authentifier avec un nom d'utilisateur et mot de passe
    Correspond à la FR6: Utilisateurs peuvent réinitialiser leur mot de passe via un processus de vérification
    """

    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service
        # Pour une implémentation complète, utiliser Redis ou une table de données
        self.tokens = {}  # Dictionnaire pour stocker les tokens en mémoire
        self.blacklisted_tokens = set()  # Ensemble pour les tokens blacklistés
        
    def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """
        Authentifie un utilisateur avec les identifiants fournis

        Args:
            credentials (dict): Identifiants de l'utilisateur (username, password)

        Returns:
            dict: Résultats de l'authentification
        """
        username = credentials.get('username')
        password = credentials.get('password')

        # Validation des entrées pour prévenir les injections
        if not username or not password:
            return {
                'authenticated': False,
                'error': 'Username and password are required'
            }

        # Validation des caractères pour prévenir les injections
        if not self._is_valid_input(username) or not self._is_valid_input(password):
            return {
                'authenticated': False,
                'error': 'Invalid characters in username or password'
            }

        # Récupérer l'utilisateur par nom d'utilisateur
        user = self.admin_service.get_user_by_username(username)

        if not user:
            # On ne distingue pas "utilisateur inexistant" de "mot de passe incorrect" pour éviter
            # les attaques par timing qui permettraient de deviner les noms d'utilisateur
            return {
                'authenticated': False,
                'error': 'Invalid credentials'
            }

        # Vérifier le mot de passe
        if not user.verify_password(password):
            return {
                'authenticated': False,
                'error': 'Invalid credentials'
            }

        # Générer un token de session
        token = self._generate_token(user)

        # Mettre à jour la date de dernier login
        self.admin_service.update_user(user.id, last_login=datetime.now())

        # Déterminer l'URL de redirection basée sur le rôle
        redirect_url = self._get_redirect_url_by_role(user.role)

        # Extraire la valeur du rôle correctement
        role_value = user.role
        if hasattr(user.role, 'value'):
            role_value = user.role.value
        elif hasattr(user.role, 'name'):
            role_value = user.role.name
        else:
            role_value = str(user.role)

        print(role_value)
        return {
            'authenticated': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': role_value,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': role_value == 'administrator'
            },
            'redirect_url': redirect_url
        }

    def _is_valid_input(self, input_str: str) -> bool:
        """
        Valide que l'entrée ne contient pas de caractères dangereux

        Args:
            input_str (str): Chaîne à valider

        Returns:
            bool: True si l'entrée est valide, False sinon
        """
        # Vérifier que l'entrée n'est pas vide
        if not input_str:
            return False

        # Vérifier la longueur maximale pour éviter les attaques par déni de service
        if len(input_str) > 255:
            return False

        # Vérifier que l'entrée ne contient pas de caractères dangereux
        # On autorise seulement les caractères alphanumériques, underscore, tiret et point
        if not re.match(r'^[a-zA-Z0-9_.@\-]+$', input_str):
            return False

        return True
    
    def _generate_token(self, user: User) -> str:
        """
        Génère un token JWT pour l'utilisateur

        Args:
            user (User): L'utilisateur authentifié

        Returns:
            str: Token JWT
        """
        # Créer les claims JWT
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Extraire la valeur du rôle correctement
        role_value = user.role
        if hasattr(user.role, 'value'):
            role_value = user.role.value
        elif hasattr(user.role, 'name'):
            role_value = user.role.name
        else:
            role_value = str(user.role)

        to_encode = {
            'sub': user.id,  # Subject: ID utilisateur
            'username': user.username,
            'role': role_value,
            'exp': expires_at,  # Expiration
            'iat': datetime.utcnow(),  # Issued at
        }

        # Générer le token JWT
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        # Stocker aussi en mémoire pour compatibilité (pourra être supprimé plus tard)
        self.tokens[token] = {
            'user_id': user.id,
            'expires_at': expires_at,
            'created_at': datetime.utcnow()
        }

        return token
    
    def _get_redirect_url_by_role(self, role) -> str:
        """
        Détermine l'URL de redirection basée sur le rôle de l'utilisateur

        Args:
            role: Rôle de l'utilisateur

        Returns:
            str: URL de redirection appropriée
        """
        role_redirect_map = {
            'administrator': '/admin/dashboard',
            'manager': '/manager/dashboard',
            'officer': '/officer/dashboard',
            'citizen': '/citizen/profile',
            'consultant': '/consultant/access'
        }

        # Extraire la valeur du rôle correctement
        role_value = role
        if hasattr(role, 'value'):
            role_value = role.value
        elif hasattr(role, 'name'):
            role_value = role.name
        else:
            role_value = str(role)

        return role_redirect_map.get(role_value, '/dashboard')
    
    def verify_token(self, token: str) -> Optional[User]:
        """
        Vérifie la validité d'un token JWT et retourne l'utilisateur associé

        Args:
            token (str): Token JWT à vérifier

        Returns:
            User: L'utilisateur si le token est valide, None sinon
        """
        # Validation du token pour prévenir les injections
        if not token or not isinstance(token, str):
            return None

        # Vérifier que le token ne contient pas de caractères suspects
        import re
        if not re.match(r'^[a-zA-Z0-9\-_=]+\.[a-zA-Z0-9\-_=]+\.?[a-zA-Z0-9\-_.+/=]*$', token):
            return None

        # Vérifier si le token est sur la liste noire
        if self.is_token_blacklisted(token):
            return None

        try:
            # Décoder le token JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                return None

            # Récupérer l'utilisateur depuis la base de données
            user = self.admin_service.get_user_by_id(user_id)
            return user

        except JWTError:
            # Token invalide ou expiré
            return None
    
    def logout(self, token: str) -> bool:
        """
        Déconnecte un utilisateur en invalidant son token

        Args:
            token (str): Token de l'utilisateur à déconnecter

        Returns:
            bool: True si la déconnexion a réussi, False sinon
        """
        # Ajouter le token à la liste noire pour invalider immédiatement
        self.blacklisted_tokens.add(token)

        # Supprimer le token du dictionnaire des tokens actifs
        if token in self.tokens:
            del self.tokens[token]

        return True

    def cleanup_expired_tokens(self):
        """
        Nettoie les tokens expirés du dictionnaire des tokens
        """
        current_time = datetime.utcnow()
        expired_tokens = []

        for token, token_info in self.tokens.items():
            if token_info.get('expires_at', current_time) < current_time:
                expired_tokens.append(token)

        for token in expired_tokens:
            del self.tokens[token]

        return len(expired_tokens)

    def is_token_blacklisted(self, token: str) -> bool:
        """
        Vérifie si un token est sur la liste noire

        Args:
            token (str): Token à vérifier

        Returns:
            bool: True si le token est blacklisté, False sinon
        """
        return token in self.blacklisted_tokens
    
    def reset_password(self, reset_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Réinitialise le mot de passe d'un utilisateur

        Args:
            reset_data (dict): Données pour la réinitialisation (email, new_password, confirmation_code)

        Returns:
            dict: Résultats de la réinitialisation du mot de passe
        """
        email = reset_data.get('email')
        new_password = reset_data.get('new_password')
        confirmation_code = reset_data.get('confirmation_code')

        # Validation des entrées pour prévenir les injections
        if not email or not new_password:
            return {
                'success': False,
                'error': 'Email and new password are required'
            }

        # Validation des caractères pour prévenir les injections
        if not self._is_valid_input(email) or not self._is_valid_input(new_password):
            return {
                'success': False,
                'error': 'Invalid characters in email or password'
            }

        # Dans une implémentation réelle, on vérifierait le code de confirmation
        # Pour l'instant, on va chercher l'utilisateur par email via le service admin
        # On parcourt tous les utilisateurs pour trouver celui avec l'email correspondant
        all_users = self.admin_service.get_all_users()
        target_user = None
        for user in all_users:
            if user.email == email:
                target_user = user
                break

        if not target_user:
            return {
                'success': False,
                'error': 'User not found'
            }

        # Mettre à jour le mot de passe via le service admin
        try:
            success = self.admin_service.update_user_password(target_user.id, new_password)
            if success:
                return {
                    'success': True,
                    'message': 'Password reset successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to update password'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error updating password: {str(e)}'
            }