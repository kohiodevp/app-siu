"""
Zone Controller - API pour la gestion des zones urbaines
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from backend.dependencies import get_current_user, get_db, require_admin
from backend.models.user import User
from backend.services.zone_service import ZoneService

router = APIRouter(prefix="/api/zones", tags=["Zones"])


class ZoneType:
    """Types de zones"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    MIXED = "mixed"
    PROTECTED = "protected"
    SPECIAL = "special"


class ZoneRequest(BaseModel):
    """Requête de création/modification de zone"""
    name: str
    code: str
    zone_type: str
    description: Optional[str] = ""
    area: float  # en hectares
    perimeter: float  # en mètres
    geometry: dict  # objet GeoJSON
    regulations: Optional[str] = ""
    allowed_uses: Optional[List[str]] = []
    restrictions: Optional[List[str]] = []


class ZoneResponse(BaseModel):
    """Réponse pour une zone"""
    success: bool
    zone_id: Optional[str] = None
    zone_info: Optional[dict] = None
    error: Optional[str] = None


@router.post("", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
def create_zone(
    zone_request: ZoneRequest,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Crée une nouvelle zone

    **Requires**: Admin or Manager role
    """
    # Validation des données d'entrée
    if not zone_request.name or len(zone_request.name.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom de la zone est requis"
        )

    if not zone_request.code or len(zone_request.code.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le code de la zone est requis"
        )

    # Valider le type de zone
    valid_zone_types = ['residential', 'commercial', 'industrial', 'agricultural', 'mixed', 'protected', 'special']
    if zone_request.zone_type not in valid_zone_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de zone invalide. Valeurs valides: {valid_zone_types}"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Préparer les données pour le service
    zone_data = {
        'name': zone_request.name,
        'code': zone_request.code,
        'zone_type': zone_request.zone_type,
        'description': zone_request.description,
        'area': zone_request.area,
        'perimeter': zone_request.perimeter,
        'geometry': zone_request.geometry,
        'regulations': zone_request.regulations,
        'allowed_uses': str(zone_request.allowed_uses) if zone_request.allowed_uses else '[]',
        'restrictions': str(zone_request.restrictions) if zone_request.restrictions else '[]',
        'created_by': current_user.id
    }

    # Appeler le service pour créer la zone
    result = zone_service.create_zone(zone_data)

    if result.get('success'):
        # Récupérer la zone créée pour la retourner
        created_zone = zone_service.get_zone_by_id(result['zone_id'])
        return ZoneResponse(
            success=True,
            zone_id=result['zone_id'],
            zone_info=created_zone
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la création de la zone')
        )


@router.get("/{zone_id}", status_code=status.HTTP_200_OK)
def get_zone(
    zone_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère les informations d'une zone

    **Requires**: Authentication
    """
    # Validation de l'ID de la zone pour prévenir les injections
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(zone_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de zone invalide"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Récupérer la zone depuis le service
    zone_info = zone_service.get_zone_by_id(zone_id)

    if not zone_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone non trouvée"
        )

    return zone_info


@router.get("", status_code=status.HTTP_200_OK)
def get_zones(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    zone_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère la liste des zones avec pagination

    **Requires**: Authentication
    """
    # Créer le service de zones
    zone_service = ZoneService(db)

    # Préparer les filtres
    filters = {}
    if zone_type:
        filters['zone_type'] = zone_type
    if search:
        filters['search'] = search

    # Récupérer les zones depuis le service
    zones = zone_service.get_zones(filters)

    # Calculer la pagination
    total = len(zones)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_zones = zones[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_zones,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.put("/{zone_id}", status_code=status.HTTP_200_OK)
def update_zone(
    zone_id: str,
    zone_request: ZoneRequest,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Met à jour les informations d'une zone existante

    **Requires**: Admin or Manager role
    """
    # Validation de l'ID de la zone
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(zone_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de zone invalide"
        )

    # Validation des données d'entrée
    if not zone_request.name or len(zone_request.name.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom de la zone est requis"
        )

    if not zone_request.code or len(zone_request.code.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le code de la zone est requis"
        )

    # Valider le type de zone
    valid_zone_types = ['residential', 'commercial', 'industrial', 'agricultural', 'mixed', 'protected', 'special']
    if zone_request.zone_type not in valid_zone_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de zone invalide. Valeurs valides: {valid_zone_types}"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Préparer les données pour le service
    zone_data = {
        'name': zone_request.name,
        'code': zone_request.code,
        'zone_type': zone_request.zone_type,
        'description': zone_request.description,
        'area': zone_request.area,
        'perimeter': zone_request.perimeter,
        'geometry': zone_request.geometry,
        'regulations': zone_request.regulations,
        'allowed_uses': str(zone_request.allowed_uses) if zone_request.allowed_uses else '[]',
        'restrictions': str(zone_request.restrictions) if zone_request.restrictions else '[]'
    }

    # Appeler le service pour mettre à jour la zone
    result = zone_service.update_zone(zone_id, zone_data)

    if result.get('success'):
        # Récupérer la zone mise à jour pour la retourner
        updated_zone = zone_service.get_zone_by_id(zone_id)
        return {
            "success": True,
            "zone_info": updated_zone
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la mise à jour de la zone')
        )


@router.delete("/{zone_id}", status_code=status.HTTP_200_OK)
def delete_zone(
    zone_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Supprime une zone

    **Requires**: Admin role
    """
    # Validation de l'ID de la zone
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(zone_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de zone invalide"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Appeler le service pour supprimer la zone
    result = zone_service.delete_zone(zone_id)

    if result.get('success'):
        return {
            "success": True,
            "zone_id": zone_id,
            "deleted_by": current_user.id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Erreur lors de la suppression de la zone')
        )


@router.get("/{zone_id}/parcels", status_code=status.HTTP_200_OK)
def get_zone_parcels(
    zone_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère les parcelles appartenant à une zone

    **Requires**: Authentication
    """
    # Validation de l'ID de la zone
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, str(zone_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de zone invalide"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Récupérer les parcelles de la zone depuis le service
    parcels = zone_service.get_zone_parcels(zone_id)

    # Calculer la pagination
    total = len(parcels)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_parcels = parcels[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_parcels,
        "total": total,
        "zone_id": zone_id,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/type/{zone_type}", status_code=status.HTTP_200_OK)
def get_zones_by_type(
    zone_type: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère les zones d'un type spécifique

    **Requires**: Authentication
    """
    # Valider le type de zone
    valid_types = ['residential', 'commercial', 'industrial', 'agricultural', 'mixed', 'protected', 'special']
    if zone_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de zone invalide. Valeurs valides: {valid_types}"
        )

    # Créer le service de zones
    zone_service = ZoneService(db)

    # Récupérer les zones du type spécifié depuis le service
    zones = zone_service.get_zones_by_type(zone_type)

    # Calculer la pagination
    total = len(zones)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_zones = zones[start_idx:end_idx]
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_zones,
        "total": total,
        "zone_type": zone_type,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }