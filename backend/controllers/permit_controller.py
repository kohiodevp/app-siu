"""
Permit Controller - API pour la gestion des permis
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from backend.dependencies import get_current_user, get_db, require_admin
from backend.models.user import User
from backend.services.permit_service import PermitService

router = APIRouter(prefix="/api/permits", tags=["Permits"])


class PermitType:
    """Types de permis disponibles"""
    CONSTRUCTION = "construction"
    OCCUPANCY = "occupancy"
    DEMOLITION = "demolition"
    SUBDIVISION = "subdivision"
    MERGER = "merger"
    CHANGE_OF_USE = "change_of_use"
    TEMPORARY = "temporary"


class PermitStatus:
    """Statuts des permis"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ACTIVE = "active"
    SUSPENDED = "suspended"


class PermitRequest(BaseModel):
    """Requête de création/modification de permis"""
    parcel_id: str
    permit_type: str
    applicant_name: str
    applicant_contact: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    attachments: Optional[List[str]] = []


class PermitResponse(BaseModel):
    """Réponse pour un permis"""
    success: bool
    permit_id: Optional[str] = None
    permit_info: Optional[dict] = None
    error: Optional[str] = None


@router.post("", response_model=PermitResponse, status_code=status.HTTP_201_CREATED)
def create_permit(
    permit_request: PermitRequest,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Crée un nouveau permis

    **Requires**: Admin or Manager role
    """
    # Validation des données d'entrée
    if not permit_request.parcel_id or len(permit_request.parcel_id.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'ID de la parcelle est requis"
        )

    if not permit_request.permit_type or len(permit_request.permit_type.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le type de permis est requis"
        )

    if not permit_request.applicant_name or len(permit_request.applicant_name.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom du demandeur est requis"
        )

    # Valider le type de permis
    valid_permit_types = ['construction', 'occupancy', 'demolition', 'subdivision', 'merger', 'change_of_use', 'temporary']
    if permit_request.permit_type not in valid_permit_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de permis invalide. Valeurs valides: {valid_permit_types}"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Préparer les données pour le service
    permit_data = {
        'parcel_id': permit_request.parcel_id,
        'permit_type': permit_request.permit_type,
        'applicant_name': permit_request.applicant_name,
        'applicant_contact': permit_request.applicant_contact,
        'description': permit_request.description,
        'start_date': permit_request.start_date.isoformat(),
        'end_date': permit_request.end_date.isoformat() if permit_request.end_date else None,
        'created_by': current_user.id
    }

    # Appeler le service pour créer le permis
    result = permit_service.create_permit(permit_data)

    if result.get('success'):
        # Récupérer le permis créé pour la retourner
        created_permit = permit_service.get_permit_by_id(result['permit_id'])
        return PermitResponse(
            success=True,
            permit_id=result['permit_id'],
            permit_info=created_permit
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la création du permis')
        )


@router.get("/{permit_id}", status_code=status.HTTP_200_OK)
def get_permit(
    permit_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère les informations d'un permis

    **Requires**: Authentication
    """
    # Validation de l'ID du permis pour prévenir les injections
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(permit_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de permis invalide"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Récupérer le permis depuis le service
    permit_info = permit_service.get_permit_by_id(permit_id)

    if not permit_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permis non trouvé"
        )

    return permit_info


@router.get("", status_code=status.HTTP_200_OK)
def get_permits(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    permit_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    parcel_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère la liste des permis avec pagination

    **Requires**: Authentication
    """
    # Créer le service de permis
    permit_service = PermitService(db)

    # Préparer les filtres
    filters = {}
    if permit_type:
        filters['permit_type'] = permit_type
    if status:
        filters['status'] = status
    if parcel_id:
        filters['parcel_id'] = parcel_id

    # Récupérer les permis depuis le service
    permits = permit_service.get_permits(filters)

    # Calculer la pagination
    total = len(permits)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_permits = permits[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_permits,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.put("/{permit_id}/approve", status_code=status.HTTP_200_OK)
def approve_permit(
    permit_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Approuve un permis en attente

    **Requires**: Admin or Manager role
    """
    # Validation de l'ID du permis
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(permit_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de permis invalide"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Appeler le service pour approuver le permis
    result = permit_service.update_permit_status(permit_id, 'approved', current_user.id)

    if result.get('success'):
        return {
            "success": True,
            "permit_id": permit_id,
            "status": "approved",
            "approved_by": current_user.id,
            "approved_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de l\'approbation du permis')
        )


@router.put("/{permit_id}/reject", status_code=status.HTTP_200_OK)
def reject_permit(
    permit_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Rejette un permis en attente

    **Requires**: Admin or Manager role
    """
    # Validation de l'ID du permis
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(permit_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de permis invalide"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Appeler le service pour rejeter le permis
    result = permit_service.update_permit_status(permit_id, 'rejected', current_user.id)

    if result.get('success'):
        return {
            "success": True,
            "permit_id": permit_id,
            "status": "rejected",
            "rejected_by": current_user.id,
            "rejected_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors du rejet du permis')
        )


@router.put("/{permit_id}/status", status_code=status.HTTP_200_OK)
def update_permit_status(
    permit_id: str,
    status: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Met à jour le statut d'un permis

    **Requires**: Admin or Manager role
    """
    # Validation de l'ID du permis
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(permit_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de permis invalide"
        )

    # Valider le statut
    valid_statuses = ['pending', 'approved', 'rejected', 'expired', 'active', 'suspended']
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statut invalide. Valeurs valides: {valid_statuses}"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Appeler le service pour mettre à jour le statut du permis
    result = permit_service.update_permit_status(permit_id, status, current_user.id)

    if result.get('success'):
        return {
            "success": True,
            "permit_id": permit_id,
            "status": status,
            "updated_by": current_user.id,
            "updated_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la mise à jour du statut du permis')
        )


@router.delete("/{permit_id}", status_code=status.HTTP_200_OK)
def delete_permit(
    permit_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Supprime un permis (uniquement ceux en attente ou rejetés)

    **Requires**: Admin role
    """
    # Validation de l'ID du permis
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(permit_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de permis invalide"
        )

    # Créer le service de permis
    permit_service = PermitService(db)

    # Appeler le service pour supprimer le permis
    result = permit_service.delete_permit(permit_id)

    if result.get('success'):
        return {
            "success": True,
            "permit_id": permit_id,
            "deleted_by": current_user.id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la suppression du permis')
        )