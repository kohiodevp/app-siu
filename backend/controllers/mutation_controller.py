"""
Contrôleur FastAPI pour la gestion des mutations de parcelles
"""

import re
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from datetime import datetime

from backend.services.mutation_service import MutationService
from backend.dependencies import get_current_user, get_db, require_admin
from backend.models.user import User

router = APIRouter(prefix="/api/mutations", tags=["Mutations"])

# Modèles Pydantic pour les requêtes/réponses
class MutationCreate(BaseModel):
    """Modèle pour créer une mutation"""
    parcel_id: str = Field(..., description="ID de la parcelle")
    mutation_type: str = Field(..., description="Type de mutation")
    from_owner_id: Optional[str] = Field(None, description="ID ancien propriétaire")
    to_owner_id: Optional[str] = Field(None, description="ID nouveau propriétaire")
    price: Optional[float] = Field(None, description="Prix de transaction", ge=0)
    notes: Optional[str] = Field(None, description="Notes additionnelles")

class MutationApprove(BaseModel):
    """Modèle pour approuver une mutation"""
    pass

class MutationReject(BaseModel):
    """Modèle pour rejeter une mutation"""
    reason: str = Field(..., description="Raison du rejet")

class MutationResponse(BaseModel):
    """Modèle de réponse pour une mutation"""
    id: str
    parcel_id: str
    mutation_type: str
    from_owner_id: Optional[str]
    to_owner_id: Optional[str]
    initiated_by_user_id: str
    price: Optional[float]
    notes: Optional[str]
    status: str
    created_at: str
    updated_at: str
    approved_at: Optional[str]
    approved_by_user_id: Optional[str]
    completed_at: Optional[str]
    rejection_reason: Optional[str]

@router.post("/", response_model=MutationResponse, status_code=status.HTTP_201_CREATED)
async def create_mutation(
    mutation: MutationCreate,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Crée une nouvelle demande de mutation de parcelle
    """
    try:
        service = MutationService(db)
        new_mutation = service.create_mutation(
            parcel_id=mutation.parcel_id,
            mutation_type=mutation.mutation_type,
            initiated_by_user_id=current_user.id,
            from_owner_id=mutation.from_owner_id,
            to_owner_id=mutation.to_owner_id,
            price=mutation.price,
            notes=mutation.notes
        )
        return new_mutation.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/", response_model=dict)
async def get_mutations(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Récupère toutes les mutations avec pagination
    """
    try:
        service = MutationService(db)
        offset = (page - 1) * page_size
        result = service.get_all_mutations(
            status=status,
            limit=page_size,
            offset=offset
        )
        
        # Convertir les mutations en dict
        result['items'] = [m.to_dict() for m in result['items']]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/{mutation_id}", response_model=MutationResponse)
async def get_mutation(
    mutation_id: str,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère une mutation par son ID
    """
    service = MutationService(db)
    mutation = service.get_mutation_by_id(mutation_id)
    if not mutation:
        raise HTTPException(status_code=404, detail="Mutation non trouvée")
    return mutation.to_dict()

@router.get("/parcel/{parcel_id}", response_model=List[MutationResponse])
async def get_parcel_mutations(
    parcel_id: str,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère toutes les mutations d'une parcelle
    """
    try:
        service = MutationService(db)
        mutations = service.get_mutations_by_parcel(parcel_id)
        return [m.to_dict() for m in mutations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/{mutation_id}/approve", response_model=MutationResponse)
async def approve_mutation(
    mutation_id: str,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Approuve une mutation
    """
    try:
        service = MutationService(db)
        mutation = service.approve_mutation(mutation_id, current_user.id)
        return mutation.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/{mutation_id}/reject", response_model=MutationResponse)
async def reject_mutation(
    mutation_id: str,
    rejection: MutationReject,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Rejette une mutation
    """
    try:
        service = MutationService(db)
        mutation = service.reject_mutation(
            mutation_id,
            current_user.id,
            rejection.reason
        )
        return mutation.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/{mutation_id}/complete", response_model=MutationResponse)
async def complete_mutation(
    mutation_id: str,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Complète une mutation (effectue le transfert)
    """
    try:
        service = MutationService(db)
        mutation = service.complete_mutation(mutation_id)
        return mutation.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/{mutation_id}/cancel", response_model=MutationResponse)
async def cancel_mutation(
    mutation_id: str,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Annule une mutation
    """
    try:
        service = MutationService(db)
        mutation = service.get_mutation_by_id(mutation_id)
        if not mutation:
            raise HTTPException(status_code=404, detail="Mutation non trouvée")

        # Vérifier que l'utilisateur peut annuler
        from backend.models.user import UserRole
        can_cancel = (
            mutation.initiated_by_user_id == current_user.id or  # Initiator
            current_user.role in [UserRole.ADMINISTRATOR, UserRole.MANAGER]  # Admin/Manager
        )

        if not can_cancel:
            raise HTTPException(status_code=403, detail="Permissions insuffisantes pour annuler cette mutation")

        mutation = service.cancel_mutation(mutation_id)
        return mutation.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
