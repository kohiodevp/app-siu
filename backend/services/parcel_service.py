from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
import asyncio
from backend.core.repository_interfaces import IParcelRepository, IParcelHistoryRepository
from backend.services.admin_service import AdminService
from backend.services.websocket_service import NotificationService
from backend.services.map_service import MapService
from backend.services.availability_service import AvailabilityService
from backend.core.exceptions import (
    EntityNotFoundException,
    InvalidDataException,
    UnauthorizedException,
    InsufficientPermissionsException,
    BusinessRuleViolationException
)
from backend.models.parcel import Parcel, ParcelCategory
from backend.models.user import User, UserRole
from backend.models.audit_log import ParcelHistory
from backend.utils.role_helpers import is_admin_or_manager, is_admin, get_role_value


class ParcelService:
    """
    Service pour la gestion des parcelles foncières avec persistance.
    Utilise le pattern Repository pour l'accès aux données.
    """

    def __init__(self, parcel_repository: IParcelRepository, parcel_history_repository: IParcelHistoryRepository, admin_service: AdminService, availability_service: AvailabilityService):
        self.parcel_repository = parcel_repository
        self.parcel_history_repository = parcel_history_repository
        self.admin_service = admin_service
        self.availability_service = availability_service
        
    def register_parcel(self, parcel_data: Dict[str, Any], created_by_user_id: str) -> Dict[str, Any]:
        """
        Enregistre une nouvelle parcelle avec les données fournies
        """
        user = self.admin_service.get_user_by_id(created_by_user_id)
        if not user:
            raise EntityNotFoundException("Utilisateur", created_by_user_id)

        if not is_admin_or_manager(user):
            raise InsufficientPermissionsException("ADMIN_OR_MANAGER_REQUIRED")

        reference_cadastrale = parcel_data['reference_cadastrale']
        if self.parcel_repository.get_by_reference(reference_cadastrale):
            raise BusinessRuleViolationException(
                "Référence cadastrale unique",
                f"Une parcelle existe déjà avec la référence cadastrale: {reference_cadastrale}"
            )

        geometry = parcel_data.get('geometry')
        if geometry:
            map_service = MapService()
            is_valid, error_msg = map_service.validate_geometry(geometry)
            if not is_valid:
                raise InvalidDataException(f'Géométrie invalide: {error_msg}', field='geometry')

        try:
            category = ParcelCategory(parcel_data.get('category', 'residential').lower())
        except ValueError:
            category = ParcelCategory.INDEFINI

        parcel = Parcel(
            reference_cadastrale=reference_cadastrale,
            coordinates_lat=parcel_data['coordinates']['lat'],
            coordinates_lng=parcel_data['coordinates']['lng'],
            area=parcel_data['area'],
            address=parcel_data['address'],
            category=category.value,
            description=parcel_data.get('description', ''),
            owner_id=parcel_data.get('owner_id'),
            cadastral_plan_ref=parcel_data.get('cadastral_plan_ref', ''),
            created_by=created_by_user_id,
            geometry=geometry
        )

        saved_parcel = self.parcel_repository.create(parcel)

        history = ParcelHistory(
            parcel_id=saved_parcel.id,
            action='creation',
            details=f'Parcelle créée avec la référence {reference_cadastrale}',
            updated_by=created_by_user_id
        )
        self.parcel_history_repository.create(history)

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(NotificationService.notify_parcel_created(
                parcel_id=saved_parcel.id,
                parcel_ref=saved_parcel.reference_cadastrale,
                created_by=created_by_user_id
            ))
        except Exception as e:
            print(f"Erreur notification WebSocket: {e}")

        return {
            'success': True,
            'parcel_id': saved_parcel.id,
            'parcel_info': saved_parcel.to_dict()
        }

    def assign_owner_to_parcel(self, parcel_id: str, owner_id: str, assigned_by_user_id: str, skip_availability_check: bool = False) -> Dict[str, Any]:
        """
        Associe un propriétaire à une parcelle
        """
        parcel = self.parcel_repository.get_by_id(parcel_id)
        if not parcel:
            raise EntityNotFoundException("Parcelle", parcel_id)

        user = self.admin_service.get_user_by_id(assigned_by_user_id)
        if not user:
            raise EntityNotFoundException("Utilisateur", assigned_by_user_id)

        if not is_admin_or_manager(user):
            raise InsufficientPermissionsException("ADMIN_OR_MANAGER_REQUIRED")

        owner = self.admin_service.get_user_by_id(owner_id)
        if not owner:
            raise EntityNotFoundException("Propriétaire", owner_id)

        if not skip_availability_check:
            availability = self.availability_service.check_availability(parcel_id, assigned_by_user_id)
            if not availability['available']:
                raise BusinessRuleViolationException(
                    "Attribution de propriétaire",
                    f'Parcelle non disponible: {availability["reason"]}'
                )

        old_owner_id = parcel.owner_id
        old_owner = self.admin_service.get_user_by_id(old_owner_id) if old_owner_id else None
        old_owner_username = old_owner.username if old_owner else "Aucun"

        parcel.owner_id = owner_id
        parcel.updated_at = datetime.now()
        updated_parcel = self.parcel_repository.update(parcel_id, parcel)

        history = ParcelHistory(
            parcel_id=parcel_id,
            action='attribution_proprietaire',
            field='owner_id',
            old_value=old_owner_id or 'None',
            new_value=owner_id,
            details=f'Propriétaire changé de "{old_owner_username}" à "{owner.username}"',
            updated_by=assigned_by_user_id
        )
        self.parcel_history_repository.create(history)

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(NotificationService.notify_parcel_updated(
                parcel_id=parcel_id,
                parcel_ref=updated_parcel.reference_cadastrale,
                updated_by=assigned_by_user_id
            ))
        except Exception as e:
            print(f"Erreur notification WebSocket: {e}")

        return {
            'success': True,
            'message': f'Propriétaire {owner.username} attribué à la parcelle {updated_parcel.reference_cadastrale}',
            'parcel_info': updated_parcel.to_dict()
        }

    def get_parcel_by_id(self, parcel_id: str) -> Optional[Parcel]:
        """Récupère une parcelle par son ID depuis la base de données"""
        return self.parcel_repository.get_by_id(parcel_id)

    def get_parcel_by_reference(self, reference_cadastrale: str) -> Optional[Parcel]:
        """Récupère une parcelle par sa référence cadastrale depuis la base de données"""
        return self.parcel_repository.get_by_reference(reference_cadastrale)
    
    def update_parcel(self, parcel_id: str, update_data: Dict[str, Any], updated_by_user_id: str) -> Dict[str, Any]:
        """Met à jour les informations d'une parcelle existante"""
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel:
            raise EntityNotFoundException("Parcelle", parcel_id)

        user = self.admin_service.get_user_by_id(updated_by_user_id)
        if not user:
            raise EntityNotFoundException("Utilisateur", updated_by_user_id)

        if not is_admin_or_manager(user):
            raise InsufficientPermissionsException("ADMIN_OR_MANAGER_REQUIRED")

        parcel.update_info(**update_data, updated_by=updated_by_user_id)
        updated_parcel = self.parcel_repository.update(parcel_id, parcel)

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(NotificationService.notify_parcel_updated(
                parcel_id=parcel_id,
                parcel_ref=updated_parcel.reference_cadastrale,
                updated_by=updated_by_user_id
            ))
        except Exception as e:
            print(f"Erreur notification WebSocket: {e}")

        return {
            'success': True,
            'parcel_info': updated_parcel.to_dict()
        }
    
    def delete_parcel(self, parcel_id: str, deleted_by_user_id: str) -> bool:
        """Supprime une parcelle de la base de données"""
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel:
            return False

        user = self.admin_service.get_user_by_id(deleted_by_user_id)
        if not user or not is_admin(user):
            return False

        parcel_ref = parcel.reference_cadastrale
        
        self.parcel_history_repository.delete_by_parcel_id(parcel_id)
        self.parcel_repository.delete(parcel_id)

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(NotificationService.notify_parcel_deleted(
                parcel_id=parcel_id,
                parcel_ref=parcel_ref,
                deleted_by=deleted_by_user_id
            ))
        except Exception as e:
            print(f"Erreur notification WebSocket: {e}")

        return True
    
    def search_parcels(self, search_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recherche des parcelles selon les critères spécifiés avec pagination.
        """
        page = search_criteria.get('page', 1)
        page_size = search_criteria.get('page_size', 100)
        
        results = self.parcel_repository.search(search_criteria)
        total = self.parcel_repository.count_search(search_criteria)
        
        return {
            'items': [p.to_dict() for p in results],
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if total > 0 else 1
        }
    
    def get_all_parcels(self) -> List[Dict[str, Any]]:
        """Récupère toutes les parcelles depuis la base de données"""
        parcels = self.parcel_repository.get_all()
        return [p.to_dict() for p in parcels]
    
    def get_parcels_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """Récupère toutes les parcelles appartenant à un propriétaire spécifique"""
        parcels = self.parcel_repository.get_by_owner(owner_id)
        return [p.to_dict() for p in parcels]
    
    def get_parcel_owners(self, parcel_id: str) -> List[Dict[str, Any]]:
        """
        Récupère les propriétaires d'une parcelle
        """
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel or not parcel.owner_id:
            return []

        owner = self.admin_service.get_user_by_id(parcel.owner_id)
        if owner:
            return [{
                'id': owner.id,
                'username': owner.username,
                'email': owner.email,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'role': owner.role.name if hasattr(owner.role, 'name') else owner.role,
                'ownership_type': 'full',
                'ownership_percentage': 100,
                'start_date': parcel.created_at.isoformat() if parcel.created_at else None,
                'end_date': None
            }]
        return []

    def get_parcel_history(self, parcel_id: str) -> List[Dict[str, Any]]:
        """
        Récupère l'historique complet d'une parcelle
        """
        history = self.parcel_history_repository.get_by_parcel_id(parcel_id)
        return [h.to_dict() for h in history]
    
    def get_all_parcels_for_map(self, current_user=None) -> List[Parcel]:
        """
        Récupère toutes les parcelles avec leur géométrie pour affichage sur carte
        """
        if current_user:
            # Vérifier le rôle de manière sécurisée
            if not is_admin_or_manager(current_user):
                return self.parcel_repository.get_by_owner(current_user.id)

        return self.parcel_repository.get_all()
    
    def update_parcel_geometry(self, parcel_id: str, geometry: List[List[float]], updated_by_user_id: str) -> Dict[str, Any]:
        """
        Met à jour uniquement la géométrie d'une parcelle
        """
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel:
            raise EntityNotFoundException("Parcelle", parcel_id)

        user = self.admin_service.get_user_by_id(updated_by_user_id)
        if not user or not is_admin_or_manager(user):
            raise InsufficientPermissionsException("Permissions insuffisantes")

        map_service = MapService()
        if not map_service.validate_geometry(geometry)[0]:
            raise InvalidDataException("Géométrie invalide")

        parcel.geometry = geometry
        parcel.updated_at = datetime.now()
        self.parcel_repository.update(parcel_id, parcel)

        history = ParcelHistory(
            parcel_id=parcel_id,
            action='modification_geometrie',
            field='geometry',
            details=f'Géométrie mise à jour avec {len(geometry)} points',
            updated_by=updated_by_user_id
        )
        self.parcel_history_repository.create(history)

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(NotificationService.notify_parcel_updated(
                parcel_id=parcel_id,
                parcel_ref=parcel.reference_cadastrale,
                updated_by=updated_by_user_id
            ))
        except Exception as e:
            print(f"Erreur notification WebSocket: {e}")

        return {
            'success': True,
            'message': 'Géométrie mise à jour',
            'parcel_id': parcel_id
        }

    def _validate_parcel_data(self, parcel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valide les données de la parcelle"""
        required_fields = ['reference_cadastrale', 'coordinates', 'area', 'address']
        
        for field in required_fields:
            if field not in parcel_data or parcel_data[field] is None:
                return {
                    'valid': False,
                    'error': f'Le champ "{field}" est requis et ne peut pas être vide'
                }
        
        reference = parcel_data['reference_cadastrale']
        if not reference or len(reference.strip()) == 0:
            return {
                'valid': False,
                'error': 'La référence cadastrale ne peut pas être vide'
            }
        
        coordinates = parcel_data['coordinates']
        if not isinstance(coordinates, dict) or 'lat' not in coordinates or 'lng' not in coordinates:
            return {
                'valid': False,
                'error': 'Les coordonnées doivent être un dictionnaire avec les clés "lat" et "lng"'
            }
        
        lat = coordinates['lat']
        lng = coordinates['lng']
        
        if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
            return {
                'valid': False,
                'error': f'Latitude invalide: {lat}. Doit être un nombre entre -90 et 90'
            }
        
        if not isinstance(lng, (int, float)) or not (-180 <= lng <= 180):
            return {
                'valid': False,
                'error': f'Longitude invalide: {lng}. Doit être un nombre entre -180 et 180'
            }
        
        area = parcel_data['area']
        if not isinstance(area, (int, float)) or area <= 0:
            return {
                'valid': False,
                'error': f'Superficie invalide: {area}. Doit être un nombre positif'
            }
        
        address = parcel_data['address']
        if not address or len(address.strip()) == 0:
            return {
                'valid': False,
                'error': 'L\'adresse ne peut pas être vide'
            }
        
        return {
            'valid': True,
            'error': None
        }

    def get_parcel_statistics(self) -> Dict[str, Any]:
        """
        Calcule et retourne les statistiques globales des parcelles

        Returns:
            Dict contenant:
            - total: Nombre total de parcelles
            - by_category: Répartition par catégorie
            - by_status: Répartition par statut
            - by_zone: Répartition par zone
            - total_area: Surface totale en m²
            - average_area: Surface moyenne en m²
        """
        all_parcels = self.parcel_repository.get_all()

        total = len(all_parcels)

        # Statistiques par catégorie
        by_category = {}
        for parcel in all_parcels:
            category = parcel.category or 'Indefini'
            by_category[category] = by_category.get(category, 0) + 1

        # Statistiques par statut
        by_status = {}
        for parcel in all_parcels:
            status = parcel.status or 'available'
            by_status[status] = by_status.get(status, 0) + 1

        # Statistiques par zone
        by_zone = {}
        for parcel in all_parcels:
            zone = parcel.zone or 'Non définie'
            by_zone[zone] = by_zone.get(zone, 0) + 1

        # Calcul des surfaces
        total_area = sum(parcel.area for parcel in all_parcels if parcel.area)
        average_area = total_area / total if total > 0 else 0

        # Trouver min et max
        areas = [parcel.area for parcel in all_parcels if parcel.area]
        min_area = min(areas) if areas else 0
        max_area = max(areas) if areas else 0

        return {
            'total': total,
            'by_category': by_category,
            'by_status': by_status,
            'by_zone': by_zone,
            'total_area': round(total_area, 2),
            'average_area': round(average_area, 2),
            'min_area': round(min_area, 2),
            'max_area': round(max_area, 2),
            'categories_count': len(by_category),
            'zones_count': len(by_zone)
        }

    def get_nearby_parcels(self, parcel_id: str, radius_km: float = 1.0) -> List[Dict[str, Any]]:
        """
        Récupère les parcelles situées à proximité d'une parcelle spécifique

        Args:
            parcel_id: ID de la parcelle de référence
            radius_km: Rayon de recherche en kilomètres (par défaut 1 km)

        Returns:
            List[Dict]: Liste des parcelles à proximité avec leurs distances
        """
        import math

        # Récupérer la parcelle de référence
        reference_parcel = self.get_parcel_by_id(parcel_id)
        if not reference_parcel:
            raise EntityNotFoundException("Parcelle", parcel_id)

        # Récupérer toutes les parcelles
        all_parcels = self.parcel_repository.get_all()

        # Calculer la distance entre la parcelle de référence et toutes les autres
        nearby_parcels = []
        for parcel in all_parcels:
            # Ne pas inclure la parcelle elle-même
            if parcel.id == parcel_id:
                continue

            # Calculer la distance en kilomètres
            distance = self._calculate_distance(
                reference_parcel.coordinates_lat, reference_parcel.coordinates_lng,
                parcel.coordinates_lat, parcel.coordinates_lng
            )

            # Ajouter à la liste si dans le rayon
            if distance <= radius_km:
                parcel_dict = parcel.to_dict()
                parcel_dict['distance_km'] = round(distance, 3)
                nearby_parcels.append(parcel_dict)

        # Trier par distance croissante
        nearby_parcels.sort(key=lambda x: x['distance_km'])

        return nearby_parcels

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcule la distance entre deux points géographiques en kilomètres
        Utilise la formule de Haversine

        Args:
            lat1, lon1: Latitude et longitude du premier point
            lat2, lon2: Latitude et longitude du deuxième point

        Returns:
            Distance en kilomètres
        """
        import math

        # Convertir les degrés en radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Différences de coordonnées
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Formule de Haversine
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        # Rayon de la Terre en km
        r = 6371

        return c * r