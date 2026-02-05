"""
Service pour la gestion des données cartographiques et la génération GeoJSON

Ce service gère:
- Génération de GeoJSON (RFC 7946) pour l'affichage cartographique
- Calcul des limites (bounds) de la carte
- Filtrage spatial des parcelles
- Validation de la géométrie
"""

from typing import List, Dict, Optional, Tuple
from backend.models.parcel import Parcel
import json


class MapService:
    """Service pour les opérations cartographiques"""
    
    def __init__(self):
        pass
    
    def generate_geojson(self, parcels: List[Parcel], include_owner_info: bool = True) -> dict:
        """
        Génère un GeoJSON FeatureCollection à partir d'une liste de parcelles
        
        Format conforme à RFC 7946: https://tools.ietf.org/html/rfc7946
        
        Args:
            parcels: Liste des parcelles à convertir
            include_owner_info: Inclure les informations du propriétaire
            
        Returns:
            dict: GeoJSON FeatureCollection
            
        Example:
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "uuid",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[lng, lat], [lng, lat], ...]]
                        },
                        "properties": {
                            "reference_cadastrale": "REF-001",
                            "area": 500.0,
                            ...
                        }
                    }
                ]
            }
        """
        features = []
        
        for parcel in parcels:
            # Créer la géométrie
            geometry = self._create_geometry(parcel)
            
            # Créer les propriétés
            properties = {
                'id': parcel.id,
                'reference': parcel.reference_cadastrale,
                'reference_cadastrale': parcel.reference_cadastrale,
                'area': parcel.area,
                'address': parcel.address,
                'category': parcel.category.value if hasattr(parcel.category, 'value') else str(parcel.category) if parcel.category else 'Indefini',
                'description': parcel.description,
                'created_at': parcel.created_at.isoformat() if hasattr(parcel.created_at, 'isoformat') else str(parcel.created_at),
                'zone': parcel.zone if hasattr(parcel, 'zone') else None,
            }
            
            # Utiliser le statut réel de la parcelle
            if hasattr(parcel, 'status') and parcel.status:
                properties['status'] = parcel.status
            elif parcel.owner_id:
                properties['status'] = 'occupied'
            else:
                properties['status'] = 'available'
            
            # Ajouter les informations du propriétaire si demandé
            if include_owner_info and parcel.owner_id:
                properties['owner_id'] = parcel.owner_id
            
            # Créer la feature
            feature = {
                'type': 'Feature',
                'id': parcel.id,
                'geometry': geometry,
                'properties': properties
            }
            
            features.append(feature)
        
        # Créer la FeatureCollection
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        return geojson
    
    def _create_geometry(self, parcel: Parcel) -> dict:
        """
        Crée l'objet geometry pour une parcelle
        
        Supporte: Polygon, MultiPolygon, et génération automatique
        
        Args:
            parcel: Parcelle
            
        Returns:
            dict: Geometry object (GeoJSON)
        """
        if parcel.geometry:
            # Cas 1: Géométrie est déjà un dict GeoJSON
            if isinstance(parcel.geometry, dict):
                if 'type' in parcel.geometry and 'coordinates' in parcel.geometry:
                    return parcel.geometry
            
            # Cas 2: Géométrie est une string JSON
            elif isinstance(parcel.geometry, str):
                import json
                try:
                    geom = json.loads(parcel.geometry)
                    if isinstance(geom, dict) and 'type' in geom and 'coordinates' in geom:
                        return geom
                except:
                    pass
            
            # Cas 3: Géométrie est une liste de coordonnées
            elif isinstance(parcel.geometry, list) and len(parcel.geometry) >= 4:
                # Détecter le format et le type
                if isinstance(parcel.geometry[0], list):
                    # Tableau imbriqué
                    if isinstance(parcel.geometry[0][0], list):
                        # MultiPolygon: [[[lon,lat],...],[[...],...]]
                        return {
                            'type': 'MultiPolygon',
                            'coordinates': [parcel.geometry]
                        }
                    else:
                        # Polygon: [[lon,lat],...]
                        return {
                            'type': 'Polygon',
                            'coordinates': [parcel.geometry]
                        }
                else:
                    # Liste simple [lon,lat,lon,lat,...] → Polygon
                    coords = []
                    for i in range(0, len(parcel.geometry), 2):
                        if i + 1 < len(parcel.geometry):
                            coords.append([parcel.geometry[i], parcel.geometry[i+1]])
                    if coords:
                        return {
                            'type': 'Polygon',
                            'coordinates': [coords]
                        }
        
        # Fallback: Générer un polygone carré à partir du point central
        if parcel.coordinates:
            lat = parcel.coordinates['lat']
            lng = parcel.coordinates['lng']
            
            # Calculer l'offset basé sur la superficie
            import math
            side_length_m = math.sqrt(parcel.area)
            
            # Conversion approximative: 1 degré de latitude ≈ 111,320 mètres
            lat_offset = (side_length_m / 2) / 111320
            
            # 1 degré de longitude varie avec la latitude
            lng_offset = (side_length_m / 2) / (111320 * math.cos(math.radians(lat)))
            
            # Créer un carré centré sur le point
            square = [
                [lng - lng_offset, lat - lat_offset],  # Sud-Ouest
                [lng + lng_offset, lat - lat_offset],  # Sud-Est
                [lng + lng_offset, lat + lat_offset],  # Nord-Est
                [lng - lng_offset, lat + lat_offset],  # Nord-Ouest
                [lng - lng_offset, lat - lat_offset]   # Fermer le polygone
            ]
            
            return {
                'type': 'Polygon',
                'coordinates': [square]
            }
        
        return None
    
    def calculate_bounds(self, parcels: List[Parcel]) -> Optional[dict]:
        """
        Calcule les limites (bounding box) d'un ensemble de parcelles
        
        Args:
            parcels: Liste des parcelles
            
        Returns:
            dict: Bounds et centre de la carte, ou None si la liste est vide
            
        Example:
            {
                "bounds": {
                    "min_lat": 45.750000,
                    "min_lng": 4.830000,
                    "max_lat": 45.770000,
                    "max_lng": 4.860000
                },
                "center": {
                    "lat": 45.760000,
                    "lng": 4.845000
                },
                "parcel_count": 42
            }
        """
        if not parcels:
            return None
        
        # Initialiser avec les coordonnées de la première parcelle
        first_parcel = parcels[0]
        min_lat = max_lat = first_parcel.coordinates['lat']
        min_lng = max_lng = first_parcel.coordinates['lng']
        
        # Parcourir toutes les parcelles pour trouver les extrema
        for parcel in parcels:
            # Si la parcelle a une géométrie, utiliser tous ses points
            if parcel.geometry:
                for point in parcel.geometry:
                    lng, lat = point
                    min_lat = min(min_lat, lat)
                    max_lat = max(max_lat, lat)
                    min_lng = min(min_lng, lng)
                    max_lng = max(max_lng, lng)
            else:
                # Sinon utiliser le point central
                lat = parcel.coordinates['lat']
                lng = parcel.coordinates['lng']
                min_lat = min(min_lat, lat)
                max_lat = max(max_lat, lat)
                min_lng = min(min_lng, lng)
                max_lng = max(max_lng, lng)
        
        # Calculer le centre
        center_lat = (min_lat + max_lat) / 2
        center_lng = (min_lng + max_lng) / 2
        
        return {
            'bounds': {
                'min_lat': min_lat,
                'min_lng': min_lng,
                'max_lat': max_lat,
                'max_lng': max_lng
            },
            'center': {
                'lat': center_lat,
                'lng': center_lng
            },
            'parcel_count': len(parcels)
        }
    
    def filter_parcels_by_bbox(self, parcels: List[Parcel], bbox: Tuple[float, float, float, float]) -> List[Parcel]:
        """
        Filtre les parcelles qui intersectent une bounding box

        Args:
            parcels: Liste des parcelles
            bbox: Tuple (min_lat, min_lng, max_lat, max_lng)

        Returns:
            List[Parcel]: Parcelles dans la bounding box
        """
        min_lat, min_lng, max_lat, max_lng = bbox
        filtered = []

        for parcel in parcels:
            # Vérifier si la parcelle intersecte la bbox
            if parcel.geometry:
                # Extraire les points de la géométrie selon son format
                points = self._extract_points_from_geometry(parcel.geometry)

                # Vérifier si au moins un point du polygone est dans la bbox
                for lng, lat in points:
                    if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng:
                        filtered.append(parcel)
                        break
            else:
                # Vérifier le point central
                lat = parcel.coordinates['lat']
                lng = parcel.coordinates['lng']
                if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng:
                    filtered.append(parcel)

        return filtered

    def _extract_points_from_geometry(self, geometry):
        """
        Extrait les points (lng, lat) d'une géométrie dans différents formats

        Args:
            geometry: Géométrie dans divers formats (dict, list, string)

        Returns:
            List[Tuple[float, float]]: Liste de points (lng, lat)
        """
        points = []

        if geometry is None:
            return points

        # Si c'est une chaîne JSON, la parser
        if isinstance(geometry, str):
            import json
            try:
                geometry = json.loads(geometry)
            except:
                return points

        # Si c'est un dictionnaire (GeoJSON), extraire les coordonnées
        if isinstance(geometry, dict):
            if 'coordinates' in geometry:
                coords = geometry['coordinates']
                # Gérer les différents types de géométries GeoJSON
                points.extend(self._extract_points_from_coordinates(coords))
        elif isinstance(geometry, list):
            # Si c'est une liste de coordonnées directes
            points.extend(self._extract_points_from_coordinates(geometry))

        return points

    def _extract_points_from_coordinates(self, coords):
        """
        Extrait les points (lng, lat) des coordonnées selon leur structure

        Args:
            coords: Coordonnées dans divers formats imbriqués

        Returns:
            List[Tuple[float, float]]: Liste de points (lng, lat)
        """
        points = []

        if coords is None:
            return points

        # Limiter la profondeur de récursion pour éviter les attaques par déni de service
        if isinstance(coords, list) and len(coords) > 10000:
            return points  # Retourner une liste vide si la structure est trop grande

        # Si c'est une liste de points [lng, lat]
        if isinstance(coords, list) and len(coords) > 0:
            # Vérifier si c'est une liste de points [lng, lat]
            if isinstance(coords[0], (int, float)) and len(coords) >= 2:
                # C'est une liste de coordonnées linéaires [lng, lat, lng, lat, ...]
                for i in range(0, len(coords), 2):
                    if i + 1 < len(coords):
                        points.append((coords[i], coords[i+1]))
            # Sinon, c'est une liste imbriquée de structures complexes
            else:
                for item in coords:
                    if isinstance(item, list):
                        # Gérer les structures imbriquées comme Polygon ou MultiPolygon
                        if len(item) > 0 and isinstance(item[0], (int, float)):
                            # C'est un point [lng, lat]
                            if len(item) >= 2:
                                points.append((item[0], item[1]))
                        else:
                            # Limiter la profondeur de récursion pour éviter les attaques par déni de service
                            if len(points) > 10000:  # Limiter le nombre total de points
                                break
                            # C'est une structure imbriquée, explorer récursivement
                            points.extend(self._extract_points_from_coordinates(item))

        return points
    
    @staticmethod
    def validate_geometry(geometry: List[List[float]]) -> Tuple[bool, Optional[str]]:
        """
        Valide une géométrie de polygone
        
        Args:
            geometry: Liste de points [[lng, lat], [lng, lat], ...]
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Vérifier que c'est une liste
        if not isinstance(geometry, list):
            return False, "La géométrie doit être une liste de coordonnées"
        
        # Vérifier le nombre minimum de points (4: 3 uniques + fermeture)
        if len(geometry) < 4:
            return False, "Un polygone doit avoir au moins 4 points (3 uniques + point de fermeture)"
        
        # Vérifier que le polygone est fermé
        if geometry[0] != geometry[-1]:
            return False, "Le polygone doit être fermé (premier point = dernier point)"
        
        # Valider chaque point
        for i, point in enumerate(geometry):
            if not isinstance(point, list) or len(point) != 2:
                return False, f"Point {i} invalide: doit être [lng, lat]"
            
            lng, lat = point
            
            if not isinstance(lng, (int, float)) or not isinstance(lat, (int, float)):
                return False, f"Point {i} invalide: les coordonnées doivent être des nombres"
            
            if not (-180 <= lng <= 180):
                return False, f"Point {i} invalide: longitude {lng} hors limites [-180, 180]"
            
            if not (-90 <= lat <= 90):
                return False, f"Point {i} invalide: latitude {lat} hors limites [-90, 90]"
        
        return True, None
    
    @staticmethod
    def generate_square_from_point(lat: float, lng: float, area_m2: float) -> List[List[float]]:
        """
        Génère un polygone carré à partir d'un point central et d'une superficie
        
        Utile pour migrer des parcelles existantes qui n'ont qu'un point central.
        
        Args:
            lat: Latitude du centre
            lng: Longitude du centre
            area_m2: Superficie en mètres carrés
            
        Returns:
            List[List[float]]: Liste de points [[lng, lat], ...] formant un carré fermé
        """
        import math
        
        # Calculer la longueur du côté
        side_length_m = math.sqrt(area_m2)
        
        # Conversion en degrés (approximation)
        lat_offset = (side_length_m / 2) / 111320  # 1 degré lat ≈ 111.32 km
        lng_offset = (side_length_m / 2) / (111320 * math.cos(math.radians(lat)))
        
        # Créer le carré (format GeoJSON: [lng, lat])
        square = [
            [lng - lng_offset, lat - lat_offset],  # Sud-Ouest
            [lng + lng_offset, lat - lat_offset],  # Sud-Est
            [lng + lng_offset, lat + lat_offset],  # Nord-Est
            [lng - lng_offset, lat + lat_offset],  # Nord-Ouest
            [lng - lng_offset, lat - lat_offset]   # Fermer le polygone
        ]
        
        return square
