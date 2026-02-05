"""
Service de gestion des zones avec SQLAlchemy
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from backend.models.zone import Zone
from backend.models.parcel import Parcel


class ZoneService:
    """Service pour la gestion des zones urbaines"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_zone(self, zone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée une nouvelle zone"""
        try:
            new_zone = Zone(
                name=zone_data['name'],
                code=zone_data['code'],
                zone_type=zone_data['zone_type'],
                description=zone_data.get('description', ''),
                area=zone_data.get('area', 0),
                perimeter=zone_data.get('perimeter', 0),
                geometry=zone_data.get('geometry'),
                regulations=zone_data.get('regulations', ''),
                allowed_uses=zone_data.get('allowed_uses'),
                restrictions=zone_data.get('restrictions'),
                created_by=zone_data.get('created_by')
            )

            self.db.add(new_zone)
            self.db.commit()
            self.db.refresh(new_zone)

            return {
                "success": True,
                "zone_id": new_zone.id
            }
        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    def get_zone_by_id(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une zone par son ID"""
        zone = self.db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            return None
        return zone.to_dict()

    def get_zones(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Récupère les zones avec filtres optionnels"""
        query = self.db.query(Zone)

        if filters:
            if filters.get('zone_type'):
                query = query.filter(Zone.zone_type == filters['zone_type'])

            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(or_(Zone.name.ilike(search_term), Zone.code.ilike(search_term)))

        zones = query.order_by(desc(Zone.created_at)).all()
        return [z.to_dict() for z in zones]

    def update_zone(self, zone_id: str, zone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour une zone existante"""
        zone = self.db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            return {"success": False, "error": "Zone not found"}

        for key, value in zone_data.items():
            if hasattr(zone, key):
                setattr(zone, key, value)
        
        zone.updated_at = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(zone)
            return {
                "success": True,
                "zone_id": zone_id
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def delete_zone(self, zone_id: str) -> Dict[str, Any]:
        """Supprime une zone"""
        zone = self.db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            return {"success": False, "error": "Zone not found"}

        try:
            self.db.delete(zone)
            self.db.commit()
            return {"success": True, "message": "Zone deleted successfully"}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_zones_by_type(self, zone_type: str) -> List[Dict[str, Any]]:
        """Récupère les zones d'un type spécifique"""
        zones = self.db.query(Zone)\
                      .filter(Zone.zone_type == zone_type)\
                      .order_by(Zone.name)\
                      .all()
        return [z.to_dict() for z in zones]

    def get_zone_parcels(self, zone_id: str) -> List[Dict[str, Any]]:
        """Récupère les parcelles appartenant à une zone"""
        # On essaie de matcher l'ID ou le Code de la zone avec le champ zone de la parcelle
        zone_obj = self.db.query(Zone).filter(Zone.id == zone_id).first()
        
        query = self.db.query(Parcel)
        if zone_obj:
            query = query.filter(or_(Parcel.zone == zone_obj.id, Parcel.zone == zone_obj.code))
        else:
            # Si zone_id n'est pas un UUID mais peut-être un code directement
            query = query.filter(Parcel.zone == zone_id)
            
        parcels = query.order_by(Parcel.reference_cadastrale).all()
        return [p.to_dict() for p in parcels]