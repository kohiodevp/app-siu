"""
Service de recherche avancée pour les parcelles et autres entités
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.core.repository_interfaces import IParcelRepository, IUserRepository, IDocumentRepository
from backend.models.parcel import Parcel
from backend.models.user import User
from backend.models.document import Document


class SearchService:
    """
    Service pour la recherche avancée avec géocodage et filtres complexes
    """
    
    def __init__(
        self,
        parcel_repository: IParcelRepository,
        user_repository: IUserRepository,
        document_repository: IDocumentRepository
    ):
        self.parcel_repository = parcel_repository
        self.user_repository = user_repository
        self.document_repository = document_repository

    def advanced_search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recherche avancée avec tous les critères possibles
        """
        # Extraire les paramètres de recherche
        query = filters.get('query', '')
        category = filters.get('category')
        status = filters.get('status')
        zone = filters.get('zone')
        min_area = filters.get('min_area')
        max_area = filters.get('max_area')
        page = filters.get('page', 1)
        page_size = filters.get('page_size', 10)
        
        # Construire les critères de recherche
        search_criteria = {
            'search_term': query,
            'category': category,
            'status': status,
            'zone': zone,
            'min_area': min_area,
            'max_area': max_area
        }
        
        # Effectuer la recherche
        parcels = self.parcel_repository.search(search_criteria)
        
        # Calculer les métadonnées de pagination
        total = len(parcels)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = parcels[start_idx:end_idx]
        
        return {
            'results': [self._parcel_to_dict(p) for p in paginated_results],
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }

    def geocode_address(self, address: str) -> List[Dict[str, Any]]:
        """
        Géocode une adresse vers des coordonnées
        """
        # Cette méthode utiliserait un service de géocodage externe comme Nominatim
        # Pour l'instant, on simule le résultat
        # En production, on utiliserait un service comme OpenStreetMap Nominatim
        import random
        # Simuler une réponse de géocodage
        return [{
            'lat': 12.3714 + random.uniform(-0.1, 0.1),
            'lng': -1.5197 + random.uniform(-0.1, 0.1),
            'address': address,
            'accuracy': 'precise',
            'provider': 'simulated'
        }]

    def reverse_geocode(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Géocode inversé - coordonnées vers adresse
        """
        # Simuler une réponse de géocodage inverse
        return {
            'address': f'Adresse simulée à {lat}, {lng}',
            'city': 'Ouagadougou',
            'country': 'Burkina Faso',
            'accuracy': 'precise'
        }

    def search_nearby(self, lat: float, lng: float, radius_km: float, limit: int) -> List[Dict[str, Any]]:
        """
        Recherche les parcelles à proximité d'un point
        """
        # Pour l'instant, on récupère toutes les parcelles et on filtre manuellement
        # En production, on utiliserait une requête spatiale avec PostGIS ou équivalent
        all_parcels = self.parcel_repository.get_all()
        
        nearby_parcels = []
        for parcel in all_parcels:
            # Calculer la distance approximative (en km) entre deux points
            # Utilisation de la formule de Haversine simplifiée
            if hasattr(parcel, 'coordinates_lat') and hasattr(parcel, 'coordinates_lng'):
                distance = self._calculate_distance(
                    lat, lng,
                    parcel.coordinates_lat,
                    parcel.coordinates_lng
                )
                if distance <= radius_km:
                    nearby_parcels.append(parcel)
                    
        # Trier par distance et limiter
        nearby_parcels.sort(key=lambda p: self._calculate_distance(
            lat, lng,
            p.coordinates_lat,
            p.coordinates_lng
        ))
        
        return [self._parcel_to_dict(p) for p in nearby_parcels[:limit]]

    def search_within_geometry(self, geometry: List[List[float]], category: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Recherche les parcelles à l'intérieur d'une géométrie
        """
        # Pour l'instant, on récupère toutes les parcelles et on vérifie manuellement
        # En production, on utiliserait une requête spatiale avec PostGIS
        all_parcels = self.parcel_repository.get_all()
        
        within_parcels = []
        for parcel in all_parcels:
            if self._is_parcel_within_geometry(parcel, geometry):
                # Vérifier les filtres additionnels
                if category and parcel.category != category:
                    continue
                if status and parcel.status != status:
                    continue
                within_parcels.append(parcel)
        
        return [self._parcel_to_dict(p) for p in within_parcels]

    def search_intersecting(self, geometry: List[List[float]], category: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Recherche les parcelles qui intersectent une géométrie
        """
        # Pour l'instant, on récupère toutes les parcelles et on vérifie manuellement
        # En production, on utiliserait une requête spatiale avec PostGIS
        all_parcels = self.parcel_repository.get_all()
        
        intersecting_parcels = []
        for parcel in all_parcels:
            if self._does_parcel_intersect_geometry(parcel, geometry):
                # Vérifier les filtres additionnels
                if category and parcel.category != category:
                    continue
                if status and parcel.status != status:
                    continue
                intersecting_parcels.append(parcel)
        
        return [self._parcel_to_dict(p) for p in intersecting_parcels]

    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calcule la distance approximative entre deux points en km
        """
        # Formule de Haversine simplifiée
        from math import radians, cos, sin, asin, sqrt
        
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        dlat = lat2 - lat1
        dlon = lng2 - lng1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Rayon de la Terre en km
        r = 6371
        
        return c * r

    def _is_parcel_within_geometry(self, parcel: Parcel, geometry: List[List[float]]) -> bool:
        """
        Vérifie si une parcelle est à l'intérieur d'une géométrie
        """
        # Pour l'instant, on vérifie simplement si les coordonnées de la parcelle
        # sont à l'intérieur du rectangle englobant de la géométrie
        if not hasattr(parcel, 'coordinates_lat') or not hasattr(parcel, 'coordinates_lng'):
            return False
            
        lat = parcel.coordinates_lat
        lng = parcel.coordinates_lng
        
        # Trouver les bornes de la géométrie
        min_lat = min(coord[1] for coord in geometry)
        max_lat = max(coord[1] for coord in geometry)
        min_lng = min(coord[0] for coord in geometry)
        max_lng = max(coord[0] for coord in geometry)
        
        return min_lat <= lat <= max_lat and min_lng <= lng <= max_lng

    def _does_parcel_intersect_geometry(self, parcel: Parcel, geometry: List[List[float]]) -> bool:
        """
        Vérifie si une parcelle intersecte une géométrie
        """
        # Pour l'instant, on utilise la même logique que _is_parcel_within_geometry
        # mais en pratique, on devrait implémenter une vraie intersection géométrique
        return self._is_parcel_within_geometry(parcel, geometry)

    def _parcel_to_dict(self, parcel: Parcel) -> Dict[str, Any]:
        """
        Convertit une parcelle en dictionnaire
        """
        return {
            'id': parcel.id,
            'reference_cadastrale': parcel.reference_cadastrale,
            'coordinates_lat': getattr(parcel, 'coordinates_lat', None),
            'coordinates_lng': getattr(parcel, 'coordinates_lng', None),
            'area': getattr(parcel, 'area', None),
            'address': getattr(parcel, 'address', None),
            'category': getattr(parcel, 'category', None),
            'status': getattr(parcel, 'status', None),
            'zone': getattr(parcel, 'zone', None),
            'owner_id': getattr(parcel, 'owner_id', None),
            'created_at': getattr(parcel, 'created_at', None),
            'updated_at': getattr(parcel, 'updated_at', None)
        }