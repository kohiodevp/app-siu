from datetime import datetime
from typing import List, Dict, Any, Optional
import html

from backend.models.alert import Alert, AlertType, AlertSeverity
from backend.core.repository_interfaces import IAlertRepository

class AlertService:
    """Service for managing alerts"""
    
    def __init__(self, alert_repository: IAlertRepository):
        self.alert_repository = alert_repository
    
    def create_alert(self, alert_type: str, parcel_id: str, message: str,
                    severity: str = 'medium', triggered_by: Optional[str] = None) -> Dict[str, Any]:
        """Create a new alert"""
        try:
            type_enum = AlertType(alert_type)
            severity_enum = AlertSeverity(severity)
            clean_message = html.escape(message)

            alert = Alert(
                alert_type=type_enum,
                parcel_id=parcel_id,
                message=clean_message,
                severity=severity_enum,
                triggered_by=triggered_by
            )

            created_alert = self.alert_repository.create(alert)
            return {'success': True, 'alert': created_alert.to_dict()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_alerts(self, acknowledged: Optional[bool] = None, severity: Optional[str] = None, limit: int = 100) -> List[Alert]:
        """Get alerts with optional filtering"""
        return self.alert_repository.get_alerts(acknowledged, severity, limit)
    
    def acknowledge_alert(self, alert_id: str, user_id: str) -> Dict[str, Any]:
        """Mark alert as acknowledged"""
        alert = self.alert_repository.get_by_id(alert_id)
        if not alert:
            return {'success': False, 'error': "Alerte non trouvée"}

        alert.acknowledge(user_id)
        
        self.alert_repository.update(alert_id, alert)
        return {'success': True, 'message': 'Alert acknowledged'}
    
    def get_alerts_for_parcel(self, parcel_id: str) -> List[Alert]:
        """Get all alerts for a specific parcel"""
        return self.alert_repository.get_alerts_for_parcel(parcel_id)
