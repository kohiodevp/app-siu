"""
Parcel controller for managing land parcels
"""
import re
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.services.parcel_service import ParcelService
from backend.services.map_service import MapService
from backend.services.availability_service import AvailabilityService
from backend.services.alert_service import AlertService
from backend.services.admin_service import AdminService
from backend.models.user import User, UserRole
from backend.dependencies import get_current_user, require_admin
from backend.container_config import get_parcel_service, get_availability_service, get_alert_service, get_admin_service
from backend.core.exceptions import SIUException
from backend.database import get_db
from sqlalchemy.orm import Session

# Pydantic models for request and response
class CoordinatesModel(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class ParcelCreateRequest(BaseModel):
    reference_cadastrale: str = Field(..., min_length=1)
    coordinates: CoordinatesModel
    area: float = Field(..., gt=0)
    address: str = Field(..., min_length=1)
    category: str = Field(default="residential")
    description: Optional[str] = ""
    geometry: Optional[List[List[float]]] = None
    owner_id: Optional[str] = None
    cadastral_plan_ref: Optional[str] = ""

class ParcelUpdateRequest(BaseModel):
    coordinates: Optional[CoordinatesModel] = None
    area: Optional[float] = Field(None, gt=0)
    address: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[str] = None
    cadastral_plan_ref: Optional[str] = None

class ParcelResponse(BaseModel):
    success: bool
    parcel_id: Optional[str] = None
    parcel_info: Optional[dict] = None
    error: Optional[str] = None

class ParcelSearchRequest(BaseModel):
    search_term: Optional[str] = ""
    reference_cadastrale: Optional[str] = ""
    address: Optional[str] = ""
    owner_id: Optional[str] = None
    category: Optional[str] = None

class GeometryUpdateRequest(BaseModel):
    geometry: List[List[float]] = Field(..., min_items=4)


# APIRouter
router = APIRouter(prefix="/api/parcels", tags=["Parcels"])

@router.post("", response_model=ParcelResponse, status_code=status.HTTP_201_CREATED)
def register_parcel(
    parcel_request: ParcelCreateRequest,
    current_user: User = Depends(require_admin),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    try:
        parcel_data = parcel_request.model_dump()
        result = parcel_service.register_parcel(parcel_data, current_user.id)
        return ParcelResponse(**result)
    except SIUException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/stats", status_code=status.HTTP_200_OK)
def get_parcel_stats(
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    """
    Récupère les statistiques globales des parcelles
    
    Returns:
        - total: Nombre total de parcelles
        - by_category: Répartition par catégorie
        - by_status: Répartition par statut
        - by_zone: Répartition par zone
        - total_area: Surface totale
        - average_area: Surface moyenne
    """
    try:
        stats = parcel_service.get_parcel_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving parcel statistics: {str(e)}"
        )

@router.get("/{parcel_id}", status_code=status.HTTP_200_OK)
def get_parcel(
    parcel_id: str,
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    parcel = parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Parcel with ID {parcel_id} not found")
    return parcel.to_dict()

@router.get("", status_code=status.HTTP_200_OK)
def get_all_parcels(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    parcels = parcel_service.get_all_parcels()
    total = len(parcels)
    start_idx = (page - 1) * page_size
    items = parcels[start_idx : start_idx + page_size]
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1
    }

@router.post("/search", status_code=status.HTTP_200_OK)
def search_parcels(
    search_request: ParcelSearchRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    search_criteria = search_request.model_dump()
    search_criteria['page'] = page
    search_criteria['page_size'] = page_size
    return parcel_service.search_parcels(search_criteria)

@router.put("/{parcel_id}", status_code=status.HTTP_200_OK)
def update_parcel(
    parcel_id: str,
    update_request: ParcelUpdateRequest,
    current_user: User = Depends(require_admin),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    update_data = update_request.model_dump(exclude_none=True)
    try:
        result = parcel_service.update_parcel(parcel_id, update_data, current_user.id)
        return result
    except SIUException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.delete("/{parcel_id}", status_code=status.HTTP_200_OK)
def delete_parcel(
    parcel_id: str,
    current_user: User = Depends(require_admin),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    success = parcel_service.delete_parcel(parcel_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Parcel with ID {parcel_id} not found or insufficient permissions")
    return {"message": f"Parcel {parcel_id} deleted successfully"}

@router.post("/{parcel_id}/owner", status_code=status.HTTP_200_OK)
def assign_owner(
    parcel_id: str,
    owner_id: str,
    current_user: User = Depends(require_admin),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    try:
        result = parcel_service.assign_owner_to_parcel(parcel_id, owner_id, current_user.id)
        return result
    except SIUException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.get("/map/geojson", status_code=status.HTTP_200_OK)
def get_parcels_geojson(
    bbox: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    owner_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    parcels = parcel_service.get_all_parcels_for_map(current_user)
    if bbox:
        try:
            coords = [float(x) for x in bbox.split(',')]
            # Create an instance of MapService to call instance methods
            map_service = MapService()
            parcels = map_service.filter_parcels_by_bbox(parcels, tuple(coords))
        except (ValueError, IndexError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bbox format. Use minLat,minLng,maxLat,maxLng")

    if category:
        # La catégorie est stockée comme chaîne dans la base de données
        parcels = [p for p in parcels if p.category == category]
    if owner_id:
        parcels = [p for p in parcels if p.owner_id == owner_id]

    # Create an instance of MapService to call instance methods
    map_service = MapService()
    return map_service.generate_geojson(parcels, include_owner_info=True)

@router.get("/map/bounds", status_code=status.HTTP_200_OK)
def get_map_bounds(
    current_user: User = Depends(get_current_user),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    parcels = parcel_service.get_all_parcels_for_map(current_user)
    if not parcels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No parcels found")
    # Create an instance of MapService to call instance methods
    map_service = MapService()
    return map_service.calculate_bounds(parcels)

@router.get("/{parcel_id}/availability", status_code=status.HTTP_200_OK)
def check_parcel_availability(
    parcel_id: str,
    current_user: User = Depends(get_current_user),
    availability_service: AvailabilityService = Depends(get_availability_service)
):
    return availability_service.check_availability(parcel_id, current_user.id)

@router.get("/{parcel_id}/status", status_code=status.HTTP_200_OK)
def get_parcel_status_detailed(
    parcel_id: str,
    availability_service: AvailabilityService = Depends(get_availability_service)
):
    return availability_service.get_parcel_status(parcel_id)

@router.post("/{parcel_id}/reserve", status_code=status.HTTP_200_OK)
def reserve_parcel(
    parcel_id: str,
    duration_minutes: int = 30,
    current_user: User = Depends(require_admin),
    availability_service: AvailabilityService = Depends(get_availability_service)
):
    result = availability_service.reserve_parcel(parcel_id, current_user.id, duration_minutes)
    if not result.get('success'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get('error', 'Reservation failed'))
    return result

@router.get("/{parcel_id}/owners", status_code=status.HTTP_200_OK)
def get_parcel_owners(
    parcel_id: str,
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    owners = parcel_service.get_parcel_owners(parcel_id)
    return {'owners': owners, 'parcel_id': parcel_id, 'count': len(owners)}

@router.get("/{parcel_id}/documents", status_code=status.HTTP_200_OK)
def get_parcel_documents(
    parcel_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    parcel_service: ParcelService = Depends(get_parcel_service),
    db: Session = Depends(get_db)
):
    """
    Récupère tous les documents d'une parcelle avec pagination
    """
    parcel = parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Parcel with ID {parcel_id} not found")
    
    # Calculer l'offset
    offset = (page - 1) * page_size
    
    # Récupérer les documents depuis la base de données
    from backend.models.document_model import Document
    query = db.query(Document).filter(Document.parcel_id == parcel_id)
    
    total = query.count()
    documents = query.offset(offset).limit(page_size).all()
    
    # Convertir en dictionnaires
    items = []
    for doc in documents:
        items.append({
            'id': doc.id,
            'filename': doc.filename,
            'file_type': doc.file_type,
            'file_size': doc.file_size,
            'file_path': doc.file_path,
            'parcel_id': doc.parcel_id,
            'uploaded_by': doc.uploaded_by,
            'uploaded_at': doc.uploaded_at.isoformat() if doc.uploaded_at else None,
            'description': doc.description
        })
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

@router.get("/{parcel_id}/history", status_code=status.HTTP_200_OK)
def get_parcel_history(
    parcel_id: str,
    current_user: User = Depends(get_current_user),
    parcel_service: ParcelService = Depends(get_parcel_service),
    admin_service: AdminService = Depends(get_admin_service)
):
    """
    Récupère l'historique d'une parcelle
    Accessible à tous les utilisateurs authentifiés
    """
    parcel = parcel_service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Parcel with ID {parcel_id} not found")

    # Autoriser l'accès à tous les utilisateurs authentifiés
    # Plus de restriction sur le rôle ou la propriété

    history = parcel_service.get_parcel_history(parcel_id)

    # Enrichir avec les noms d'utilisateurs
    enriched_history = []
    for entry in history:
        user_id = entry.get('updated_by')
        user_name = 'Système'
        if user_id:
            user = admin_service.get_user_by_id(user_id)
            if user:
                user_name = user.name or user.username

        # Ajouter des informations supplémentaires
        entry['user_name'] = user_name
        entry['action_label'] = entry.get('action', 'Modification').capitalize()
        enriched_history.append(entry)

    return {
        'history': enriched_history,
        'parcel_reference': parcel.reference_cadastrale if hasattr(parcel, 'reference_cadastrale') else str(parcel.id),
        'count': len(enriched_history)
    }

@router.get("/{parcel_id}/nearby", status_code=status.HTTP_200_OK)
def get_nearby_parcels(
    parcel_id: str,
    radius: float = Query(1.0, ge=0.1, le=10.0, description="Rayon de recherche en kilomètres (0.1 à 10.0)"),
    current_user: User = Depends(get_current_user),
    parcel_service: ParcelService = Depends(get_parcel_service)
):
    """
    Récupère les parcelles situées à proximité d'une parcelle spécifique
    
    Args:
        parcel_id: ID de la parcelle de référence
        radius: Rayon de recherche en kilomètres (0.1 à 10.0)
    """
    try:
        nearby_parcels = parcel_service.get_nearby_parcels(parcel_id, radius)
        return {
            'parcel_id': parcel_id,
            'radius_km': radius,
            'count': len(nearby_parcels),
            'parcels': nearby_parcels
        }
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/verification-log", status_code=status.HTTP_200_OK)
def get_verification_history(
    parcel_id: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    availability_service: AvailabilityService = Depends(get_availability_service)
):
    history = availability_service.get_verification_history(parcel_id, limit)
    return {'verification_log': history, 'count': len(history)}

@router.get("/alerts", status_code=status.HTTP_200_OK)
def get_alerts(
    acknowledged: Optional[bool] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    alert_service: AlertService = Depends(get_alert_service)
):
    alerts = alert_service.get_alerts(acknowledged, severity, limit)
    return {'alerts': [alert.to_dict() for alert in alerts], 'count': len(alerts)}
