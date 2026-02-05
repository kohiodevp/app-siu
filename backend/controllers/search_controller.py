"""
Controller de recherche spatiale pour le système SIU
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from pydantic import BaseModel

from backend.services.search_service import SearchService
from backend.models.user import User
from backend.dependencies import get_current_user
from backend.container_config import get_search_service


class CoordinatesModel(BaseModel):
    lat: float = Query(..., ge=-90, le=90, description="Latitude")
    lng: float = Query(..., ge=-180, le=180, description="Longitude")


class NearbySearchRequest(BaseModel):
    lat: float = Query(..., ge=-90, le=90, description="Latitude du point central")
    lng: float = Query(..., ge=-180, le=180, description="Longitude du point central")
    radius_km: float = Query(1.0, ge=0.1, le=10.0, description="Rayon de recherche en kilomètres")
    limit: int = Query(50, ge=1, le=1000, description="Nombre maximum de résultats")


class GeocodeRequest(BaseModel):
    address: str = Query(..., min_length=1, description="Adresse à géocoder")


class ReverseGeocodeRequest(BaseModel):
    lat: float = Query(..., ge=-90, le=90, description="Latitude")
    lng: float = Query(..., ge=-180, le=180, description="Longitude")


# APIRouter
router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/nearby", status_code=status.HTTP_200_OK)
def search_nearby_parcels(
    lat: float = Query(..., ge=-90, le=90, description="Latitude du point central"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude du point central"),
    radius_km: float = Query(1.0, ge=0.1, le=10.0, description="Rayon de recherche en kilomètres"),
    limit: int = Query(50, ge=1, le=1000, description="Nombre maximum de résultats"),
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Recherche les parcelles à proximité d'un point géographique
    
    Args:
        lat: Latitude du point central
        lng: Longitude du point central
        radius_km: Rayon de recherche en kilomètres
        limit: Nombre maximum de résultats à retourner
    """
    try:
        nearby_parcels = search_service.search_nearby(lat, lng, radius_km, limit)
        return {
            'results': nearby_parcels,
            'center_point': {'lat': lat, 'lng': lng},
            'radius_km': radius_km,
            'count': len(nearby_parcels)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche de parcelles à proximité: {str(e)}"
        )


@router.post("/geocode", status_code=status.HTTP_200_OK)
def geocode_address(
    request: GeocodeRequest,
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Géocode une adresse vers des coordonnées géographiques
    """
    try:
        results = search_service.geocode_address(request.address)
        return {
            'results': results,
            'query': request.address,
            'count': len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du géocodage: {str(e)}"
        )


@router.post("/reverse-geocode", status_code=status.HTTP_200_OK)
def reverse_geocode(
    request: ReverseGeocodeRequest,
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Géocode inversé - convertit des coordonnées en adresse
    """
    try:
        result = search_service.reverse_geocode(request.lat, request.lng)
        return {
            'result': result,
            'coordinates': {'lat': request.lat, 'lng': request.lng}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du géocodage inverse: {str(e)}"
        )


@router.post("/within", status_code=status.HTTP_200_OK)
def search_within_geometry(
    geometry: List[List[float]],
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Recherche les parcelles à l'intérieur d'une géométrie
    
    Args:
        geometry: Liste de coordonnées [longitude, latitude] définissant un polygone
        category: Filtre par catégorie de parcelle
        status: Filtre par statut de parcelle
    """
    if len(geometry) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La géométrie doit contenir au moins 3 points pour former un polygone"
        )

    try:
        results = search_service.search_within_geometry(geometry, category, status)
        return {
            'results': results,
            'geometry': geometry,
            'filters': {
                'category': category,
                'status': status
            },
            'count': len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche dans la géométrie: {str(e)}"
        )


@router.post("/intersect", status_code=status.HTTP_200_OK)
def search_intersecting_geometry(
    geometry: List[List[float]],
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Recherche les parcelles qui intersectent une géométrie
    
    Args:
        geometry: Liste de coordonnées [longitude, latitude] définissant un polygone
        category: Filtre par catégorie de parcelle
        status: Filtre par statut de parcelle
    """
    if len(geometry) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La géométrie doit contenir au moins 3 points pour former un polygone"
        )

    try:
        results = search_service.search_intersecting(geometry, category, status)
        return {
            'results': results,
            'geometry': geometry,
            'filters': {
                'category': category,
                'status': status
            },
            'count': len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche d'intersection: {str(e)}"
        )