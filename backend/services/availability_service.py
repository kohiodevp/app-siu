from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from backend.models.parcel import Parcel
from backend.models.availability import ParcelReservation, VerificationLog
from backend.models.user import UserRole
from backend.core.repository_interfaces import (
    IParcelRepository,
    IParcelReservationRepository,
    IVerificationLogRepository
)
from backend.services.admin_service import AdminService
from backend.services.alert_service import AlertService

class AvailabilityService:
    """Service for checking parcel availability and preventing double attribution"""
    
    def __init__(self, 
                 parcel_repo: IParcelRepository, 
                 reservation_repo: IParcelReservationRepository,
                 log_repo: IVerificationLogRepository,
                 admin_service: AdminService, 
                 alert_service: AlertService):
        self.parcel_repo = parcel_repo
        self.reservation_repo = reservation_repo
        self.log_repo = log_repo
        self.admin_service = admin_service
        self.alert_service = alert_service
        self.default_reservation_minutes = 30
    
    def check_availability(self, parcel_id: str, checked_by: str) -> Dict[str, Any]:
        """Check if parcel is available for attribution"""
        parcel = self.parcel_repo.get_by_id(parcel_id)

        if not parcel:
            result = {'available': False, 'reason': 'Parcelle non trouvée', 'status': 'not_found'}
            self._log_verification(parcel_id, checked_by, 'unavailable', 'Parcelle non trouvée')
            return result

        if parcel.owner_id:
            result = {'available': False, 'reason': 'Parcelle déjà attribuée', 'status': 'assigned', 'owner_id': parcel.owner_id}
            alert_message = f"Tentative d'attribution sur parcelle déjà attribuée à l'utilisateur {parcel.owner_id[:8]}..."
            self.alert_service.create_alert('double_attribution_attempt', parcel_id,
                alert_message, 'high', checked_by)
            self._log_verification(parcel_id, checked_by, 'unavailable', 'Déjà attribuée', f'Owner: {parcel.owner_id}')
            return result

        reservation = self.reservation_repo.get_active_reservation(parcel_id)
        if reservation:
            result = {'available': False, 'reason': 'Parcelle réservée', 'status': 'reserved',
                     'reserved_by': reservation.reserved_by, 'expires_at': reservation.expires_at.isoformat()}
            self._log_verification(parcel_id, checked_by, 'unavailable', 'Réservée', f'Reserved by: {reservation.reserved_by[:8]}...')
            return result

        result = {'available': True, 'reason': 'Parcelle disponible', 'status': 'available',
                 'parcel_id': parcel_id, 'reference': parcel.reference_cadastrale}
        self._log_verification(parcel_id, checked_by, 'available', 'Disponible')
        return result

    def get_parcel_status(self, parcel_id: str) -> Dict[str, Any]:
        """Get detailed parcel status"""
        parcel = self.parcel_repo.get_by_id(parcel_id)
        
        if not parcel:
            return {'status': 'not_found', 'message': 'Parcelle non trouvée'}
        
        status = {
            'parcel_id': parcel_id, 
            'reference': parcel.reference_cadastrale,
            'owner_id': parcel.owner_id, 
            'status': 'available' if not parcel.owner_id else 'assigned'
        }
        
        reservation = self.reservation_repo.get_active_reservation(parcel_id)
        if reservation:
            status['status'] = 'reserved'
            status['reservation'] = {
                'id': reservation.id,
                'reserved_by': reservation.reserved_by,
                'expires_at': reservation.expires_at.isoformat()
            }
        
        return status
    
    def reserve_parcel(self, parcel_id: str, reserved_by: str, duration_minutes: Optional[int] = None) -> Dict[str, Any]:
        """Temporarily reserve a parcel"""
        user = self.admin_service.get_user_by_id(reserved_by)
        if not user or user.role.name not in [UserRole.ADMINISTRATOR.value, UserRole.MANAGER.value]:
            return {'success': False, 'error': 'Permissions insuffisantes'}

        availability = self.check_availability(parcel_id, reserved_by)
        if not availability['available']:
            return {'success': False, 'error': availability['reason']}

        duration = duration_minutes or self.default_reservation_minutes
        if duration > 480:
            return {'success': False, 'error': 'Durée trop longue (max 8h)'}

        reserved_at = datetime.now()
        expires_at = reserved_at + timedelta(minutes=duration)

        reservation = ParcelReservation(
            parcel_id=parcel_id,
            reserved_by=reserved_by,
            reserved_at=reserved_at,
            expires_at=expires_at,
            is_active=True
        )
        created_reservation = self.reservation_repo.create(reservation)
        return {'success': True, 'reservation_id': created_reservation.id, 'expires_at': expires_at.isoformat()}
    
    def _log_verification(self, parcel_id: str, checked_by: str, result: str, reason: str, conflict_details: Optional[str] = None):
        """Log a verification check"""
        log = VerificationLog(
            parcel_id=parcel_id,
            checked_by=checked_by,
            check_timestamp=datetime.now(),
            result=result,
            reason=reason,
            conflict_details=conflict_details
        )
        self.log_repo.create(log)
    
    def get_verification_history(self, parcel_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get verification history"""
        if parcel_id:
            logs = self.log_repo.get_by_parcel_id(parcel_id, limit)
        else:
            logs = self.log_repo.get_all_with_limit(limit)
        return [l.to_dict() for l in logs]
