"""
Authentication controller for login/logout endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import Optional

from backend.services.auth_service import AuthService
from backend.models.user import User
from backend.dependencies import get_current_user, security

# Pydantic models for request and response
class LoginRequest(BaseModel):
    """Modèle de données pour la requête de connexion."""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Modèle de données pour la réponse de connexion réussie."""
    authenticated: bool
    token: str
    user: dict
    redirect_url: str

class ErrorResponse(BaseModel):
    """Modèle de données pour les erreurs d'authentification."""
    authenticated: bool = False
    error: str

# APIRouter
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def get_auth_service():
    from backend.container_config import get_admin_service
    admin_service = get_admin_service()
    return AuthService(admin_service=admin_service)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Authentifie un utilisateur avec username et password.
    
    Retourne un token JWT si les identifiants sont valides.
    
    **Acceptance Criteria:**
    - AC1: L'utilisateur peut se connecter avec ses identifiants
    - AC2: Le système vérifie la validité des identifiants
    - AC3: Le système redirige l'utilisateur vers la page appropriée selon son rôle
    
    **Returns:**
    - 200: Authentification réussie avec token JWT
    - 401: Identifiants invalides
    """
    credentials = {
        'username': login_request.username,
        'password': login_request.password
    }
    
    # Appeler le service d'authentification
    result = auth_service.authenticate(credentials)
    
    # Vérifier si l'authentification a réussi
    if not result.get('authenticated', False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get('error', 'Invalid credentials'),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retourner la réponse avec le token JWT
    return LoginResponse(
        authenticated=True,
        token=result['token'],
        user=result['user'],
        redirect_url=result['redirect_url']
    )

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), current_user: User = Depends(get_current_user)):
    """
    Déconnecte l'utilisateur actuellement authentifié.

    Nécessite un token JWT valide dans le header Authorization.

    **Note:** Avec notre implémentation, le logout côté serveur invalide le token
    en l'ajoutant à une liste noire, ce qui empêche son utilisation future.

    **Returns:**
    - 200: Déconnexion réussie
    - 401: Token invalide ou expiré
    """
    # Obtenir le service d'authentification
    from backend.container_config import get_admin_service
    admin_service = get_admin_service()
    auth_service = AuthService(admin_service=admin_service)

    # Invalider le token côté serveur en l'ajoutant à la liste noire
    auth_service.logout(credentials.credentials)

    return {
        "message": "Successfully logged out",
        "user_id": current_user.id,
        "username": current_user.username
    }

@router.get("/me", status_code=status.HTTP_200_OK)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur actuellement authentifié.

    Utile pour vérifier la validité d'un token et récupérer le profil.

    **Returns:**
    - 200: Informations de l'utilisateur
    - 401: Token invalide ou expiré
    """
    # Extraire la valeur du rôle correctement
    role_value = current_user.role
    if hasattr(current_user.role, 'value'):
        role_value = current_user.role.value
    elif hasattr(current_user.role, 'name'):
        role_value = current_user.role.name
    else:
        role_value = str(current_user.role)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": role_value,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_active": current_user.is_active
    }
