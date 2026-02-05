"""
Service de gestion des permis avec SQLAlchemy
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.models.permit import Permit


class PermitService:
    """Service pour la gestion des permis"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_permit(self, permit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un nouveau permis"""
        try:
            # Conversion des dates si elles sont fournies en string
            start_date = permit_data['start_date']
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)
            
            end_date = permit_data.get('end_date')
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date)

            new_permit = Permit(
                parcel_id=permit_data['parcel_id'],
                permit_type=permit_data['permit_type'],
                applicant_name=permit_data['applicant_name'],
                applicant_contact=permit_data.get('applicant_contact'),
                description=permit_data.get('description'),
                start_date=start_date,
                end_date=end_date,
                status='pending',
                created_by=permit_data.get('created_by')
            )

            self.db.add(new_permit)
            self.db.commit()
            self.db.refresh(new_permit)

            return {
                "success": True,
                "permit_id": new_permit.id
            }
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    def get_permit_by_id(self, permit_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un permis par son ID"""
        permit = self.db.query(Permit).filter(Permit.id == permit_id).first()
        if not permit:
            return None
        return permit.to_dict()

    def get_permits(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Récupère les permis avec filtres optionnels"""
        query = self.db.query(Permit)

        if filters:
            if filters.get('permit_type'):
                query = query.filter(Permit.permit_type == filters['permit_type'])
            if filters.get('status'):
                query = query.filter(Permit.status == filters['status'])
            if filters.get('parcel_id'):
                query = query.filter(Permit.parcel_id == filters['parcel_id'])

        permits = query.order_by(desc(Permit.created_at)).all()
        return [p.to_dict() for p in permits]

    def update_permit_status(self, permit_id: str, status: str, updated_by: str) -> Dict[str, Any]:
        """Met à jour le statut d'un permis"""
        permit = self.db.query(Permit).filter(Permit.id == permit_id).first()
        if not permit:
            return {"success": False, "error": "Permit not found"}

        permit.status = status
        # On pourrait aussi enregistrer qui a mis à jour (approved_by / rejected_by)
        if status == 'approved':
            permit.approved_by = updated_by
            permit.approved_at = datetime.now()
        elif status == 'rejected':
            permit.rejected_by = updated_by
            permit.rejected_at = datetime.now()

        try:
            self.db.commit()
            return {
                "success": True,
                "permit_id": permit_id,
                "status": status
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def delete_permit(self, permit_id: str) -> Dict[str, Any]:
        """Supprime un permis"""
        permit = self.db.query(Permit).filter(Permit.id == permit_id).first()
        if not permit:
            return {"success": False, "error": "Permit not found"}

        try:
            self.db.delete(permit)
            self.db.commit()
            return {"success": True, "message": "Permit deleted successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}