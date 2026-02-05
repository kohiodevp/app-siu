from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# from backend.services.admin_service import AdminService # Will be injected via Depends
from backend.models.user import UserRole, User # User is kept for type hinting in Depends
from backend.dependencies import require_admin, get_current_user
from sqlalchemy.orm import Session # Import Session
from backend.database import get_db # Import get_db

# Pydantic models for request and response
class UserCreateRequest(BaseModel):
    """Modèle de données pour la requête de création d'utilisateur."""
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_.@\-]+$')
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default='citizen', pattern=r'^[a-z_]+$')
    first_name: Optional[str] = Field(None, max_length=50, pattern=r'^[a-zA-Z\s\-\'\.]*$')
    last_name: Optional[str] = Field(None, max_length=50, pattern=r'^[a-zA-Z\s\-\'\.]*$')


class UserResponse(BaseModel):
    """Modèle de données pour la réponse utilisateur (sans le mot de passe)."""
    id: str
    username: str
    email: EmailStr  # Changed to EmailStr
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    """Modèle de réponse paginée"""
    items: List[UserResponse]
    total: int
    skip: int
    limit: int

class UserUpdateRequest(BaseModel):
    """Modèle de données pour la requête de mise à jour d'utilisateur."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50, pattern=r'^[a-zA-Z\s\-\'\.]*$')
    last_name: Optional[str] = Field(None, max_length=50, pattern=r'^[a-zA-Z\s\-\'\.]*$')


# APIRouter
router = APIRouter()

# Dependency for UserService
def get_user_service(db: Session = Depends(get_db)) -> "UserService":
    # Local import to avoid circular dependency
    from backend.services.user_service import UserService
    return UserService(db)

# Dependency for AdminService
def get_admin_service(db: Session = Depends(get_db)) -> "AdminService":
    # Local import to avoid circular dependency
    from backend.services.admin_service import AdminService
    return AdminService(db)


@router.get("/api/users", response_model=PaginatedResponse, status_code=status.HTTP_200_OK, tags=["Users"])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_admin: User = Depends(require_admin),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Récupère la liste de tous les utilisateurs avec pagination et filtres.
    Accessible uniquement par les administrateurs authentifiés.

    Requires:
        - Authentication: Bearer token (JWT)
        - Role: Administrator
    """
    try:
        # Récupérer les utilisateurs avec les filtres et la pagination
        users = user_service.get_users_with_filters(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            role=role,
            is_active=is_active
        )

        # Compter le nombre total d'utilisateurs pour la pagination
        total_users = user_service.count_users_with_filters(
            search=search,
            role=role,
            is_active=is_active
        )

        return PaginatedResponse(
            items=[UserResponse.model_validate(user) for user in users], # Use model_validate
            total=total_users,
            skip=skip,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des utilisateurs: {str(e)}"
        )


@router.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_new_user(
    user_request: UserCreateRequest,
    current_admin: User = Depends(require_admin),
    admin_service: "AdminService" = Depends(get_admin_service) # Inject AdminService
):
    """
    Crée un nouvel utilisateur dans le système.
    Accessible uniquement par les administrateurs authentifiés.

    Requires:
        - Authentication: Bearer token (JWT)
        - Role: Administrator
    """
    try:
        # Validation des champs pour prévenir les injections - Pydantic handles most now
        # user_request.validate_fields() # Removed, as Pydantic handles it

        # Convertir le modèle Pydantic en dictionnaire
        user_data = user_request.model_dump() # Use model_dump for Pydantic v2

        # Valider que le rôle demandé est valide et que l'administrateur a le droit de l'attribuer
        requested_role = user_data.get('role', UserRole.CITIZEN.value) # Default to UserRole enum value

        # Seuls les administrateurs peuvent créer des utilisateurs avec des rôles élevés
        if requested_role.lower() in [UserRole.ADMINISTRATOR.value] and current_admin.role.name != UserRole.ADMINISTRATOR.value: # Check role.name
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create administrator accounts"
            )

        # Appeler le service pour créer l'utilisateur
        new_user = admin_service.create_user(user_data) # Use injected service

        return UserResponse.model_validate(new_user) # Direct conversion

    except ValueError as e:
        # Si le service lève une ValueError (ex: utilisateur dupliqué, rôle invalide),
        # retourner une erreur HTTP 400.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Ré-émettre les exceptions HTTP existantes
        raise
    except Exception as e:
        # Pour toute autre erreur inattendue
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur interne est survenue: {str(e)}"
        )


@router.get("/api/users/roles/stats", status_code=status.HTTP_200_OK, tags=["Users"])
def get_role_statistics(
    current_admin: User = Depends(require_admin),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Récupère les statistiques des rôles utilisateurs.
    
    Requires:
        - Authentication: Bearer token (JWT)
        - Role: Administrator
    """
    stats = user_service.get_role_statistics()
    
    return {
        "success": True,
        "data": stats
    }


@router.put("/api/users/{user_id}", response_model=dict, status_code=status.HTTP_200_OK, tags=["Users"])
def update_user_profile(
    user_id: str,
    user_request: UserUpdateRequest, # Use the new Pydantic model
    current_user: User = Depends(get_current_user),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Met à jour le profil d'un utilisateur.
    L'utilisateur peut modifier son propre profil.

    Requires:
        - Authentication: Bearer token (JWT)
    """
    # FastAPI path parameter validation (for UUID format) can be added here if needed
    # or rely on the service to validate if user_id is a valid UUID before querying.

    # Vérifier que l'utilisateur modifie son propre profil ou est admin
    if current_user.id != user_id and not current_user.role.name == UserRole.ADMINISTRATOR.value: # Simplified role check
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    # Convertir le modèle Pydantic en dictionnaire, excluant les champs non définis
    update_data = user_request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )

    try:
        # Utiliser le service pour mettre à jour l'utilisateur
        updated_user = user_service.update_profile(user_id, update_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "success": True,
            "message": "Profile updated successfully",
            "user": UserResponse.model_validate(updated_user) # Direct conversion
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )


@router.put("/api/users/{user_id}/role", response_model=dict, status_code=status.HTTP_200_OK, tags=["Users"])
def update_user_role(
    user_id: str,
    role_name: str,
    current_admin: User = Depends(require_admin),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Met à jour le rôle d'un utilisateur.
    
    Requires:
        - Authentication: Bearer token (JWT)
        - Role: Administrator
    """
    try:
        updated_user = user_service.update_user_role(user_id, role_name, current_admin.id)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "success": True,
            "message": "User role updated successfully",
            "user": UserResponse.model_validate(updated_user) # Direct conversion
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/api/users/permissions/{role_name}", status_code=status.HTTP_200_OK, tags=["Users"])
def get_permissions_for_role(
    role_name: str,
    current_admin: User = Depends(require_admin),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Récupère les permissions associées à un rôle.
    
    Requires:
        - Authentication: Bearer token (JWT)
        - Role: Administrator
    """
    permissions = user_service.get_permissions_for_role(role_name)
    
    return {
        "success": True,
        "role": role_name,
        "permissions": permissions
    }


class ChangePasswordRequest(BaseModel):
    """Modèle pour la requête de changement de mot de passe"""
    current_password: str
    new_password: str


@router.post("/api/users/change-password", status_code=status.HTTP_200_OK, tags=["Users"])
def change_user_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    user_service: "UserService" = Depends(get_user_service) # Inject UserService
):
    """
    Change le mot de passe de l'utilisateur courant.

    Requires:
        - Authentication: Bearer token (JWT)
    """
    try:
        success = user_service.change_password(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        return {
            "success": True,
            "message": "Password changed successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error changing password: {str(e)}"
        )
