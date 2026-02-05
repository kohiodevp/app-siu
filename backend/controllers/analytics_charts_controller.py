"""
Analytics Charts Controller - API pour les données des graphiques analytiques
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import re

from backend.dependencies import get_current_user, get_db, require_admin
from backend.services.analytics_service import AnalyticsService
from backend.models.user import User

router = APIRouter(prefix="/api/analytics", tags=["Analytics Charts"])


@router.get("/parcels/status", status_code=status.HTTP_200_OK)
def get_parcel_status_distribution(
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère la distribution des parcelles par statut

    **Requires**: Admin role
    """
    try:
        cursor = db.cursor()
        
        # Compter les parcelles par statut
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN status IS NULL THEN 'available'
                    ELSE status 
                END as status,
                COUNT(*) as count
            FROM parcels
            GROUP BY status
        """)
        
        rows = cursor.fetchall()
        
        # Initialiser les compteurs
        result = {
            "available": 0,
            "occupied": 0,
            "disputed": 0,
            "reserved": 0
        }
        
        # Remplir les résultats
        for row in rows:
            status_key = row[0]
            if status_key in result:
                result[status_key] = row[1]
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la distribution des parcelles par statut : {str(e)}"
        )


@router.get("/parcels/trends", status_code=status.HTTP_200_OK)
def get_parcel_trends(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser"),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les tendances des parcelles (créations/modifications) sur une période

    **Requires**: Admin role
    """
    try:
        cursor = db.cursor()
        
        # Calculer la date de début
        start_date = datetime.now() - timedelta(days=days)
        
        # Récupérer les parcelles créées par date
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as created
            FROM parcels
            WHERE created_at >= ?
            GROUP BY DATE(created_at)
            ORDER BY date
        """, (start_date.isoformat(),))
        
        created_rows = cursor.fetchall()
        
        # Récupérer les modifications par date (depuis l'historique)
        cursor.execute("""
            SELECT 
                DATE(timestamp) as date,
                COUNT(*) as updated
            FROM parcel_history
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, (start_date.isoformat(),))
        
        updated_rows = cursor.fetchall()
        
        # Fusionner les données
        date_map = {}
        
        for row in created_rows:
            date_str = row[0]
            date_map[date_str] = {"date": date_str, "created": row[1], "updated": 0}
        
        for row in updated_rows:
            date_str = row[0]
            if date_str in date_map:
                date_map[date_str]["updated"] = row[1]
            else:
                date_map[date_str] = {"date": date_str, "created": 0, "updated": row[1]}
        
        # Convertir en liste triée par date
        result = sorted(list(date_map.values()), key=lambda x: x["date"])
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des tendances des parcelles : {str(e)}"
        )


@router.get("/documents/types", status_code=status.HTTP_200_OK)
def get_document_types_distribution(
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère la distribution des documents par type

    **Requires**: Admin role
    """
    try:
        cursor = db.cursor()
        
        # Compter les documents par type
        cursor.execute("""
            SELECT 
                document_type,
                COUNT(*) as count
            FROM documents
            GROUP BY document_type
            ORDER BY count DESC
        """)
        
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "type": row[0],
                "count": row[1]
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la distribution des documents par type : {str(e)}"
        )


@router.get("/users/activity", status_code=status.HTTP_200_OK)
def get_user_activity(
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère l'activité des utilisateurs par jour de la semaine

    **Requires**: Admin role
    """
    try:
        cursor = db.cursor()
        
        # Récupérer l'activité des utilisateurs par jour de la semaine
        cursor.execute("""
            SELECT 
                strftime('%w', timestamp) as day_of_week,
                COUNT(*) as activity
            FROM audit_logs
            WHERE timestamp >= date('now', '-7 days')
            GROUP BY strftime('%w', timestamp)
            ORDER BY day_of_week
        """)
        
        rows = cursor.fetchall()
        
        # Mapper les numéros de jour vers les noms
        day_names = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"]
        
        result = []
        for i in range(7):
            day_found = False
            for row in rows:
                if int(row[0]) == i:
                    result.append({
                        "day": day_names[i],
                        "activity": row[1]
                    })
                    day_found = True
                    break
            if not day_found:
                result.append({
                    "day": day_names[i],
                    "activity": 0
                })
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'activité des utilisateurs : {str(e)}"
        )


@router.get("/parcels/geographic", status_code=status.HTTP_200_OK)
def get_geographic_distribution(
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère la distribution géographique des parcelles

    **Requires**: Admin role
    """
    try:
        cursor = db.cursor()
        
        # Compter les parcelles par zone géographique
        # Note: Cette requête suppose que vous avez un champ "zone" dans la table parcels
        # Si ce champ n'existe pas, vous pouvez baser la distribution sur d'autres critères
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN coordinates_lat BETWEEN 0 AND 10 THEN 'Zone Sud'
                    WHEN coordinates_lat BETWEEN 10 AND 20 THEN 'Zone Centre Sud'
                    WHEN coordinates_lat BETWEEN 20 AND 30 THEN 'Zone Centre'
                    WHEN coordinates_lat BETWEEN 30 AND 40 THEN 'Zone Centre Nord'
                    WHEN coordinates_lat > 40 THEN 'Zone Nord'
                    ELSE 'Zone Inconnue'
                END as zone,
                COUNT(*) as count
            FROM parcels
            GROUP BY zone
            ORDER BY count DESC
        """)
        
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "zone": row[0],
                "count": row[1]
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la distribution géographique des parcelles : {str(e)}"
        )