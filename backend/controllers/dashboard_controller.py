"""
Dashboard Controller - API endpoints pour statistiques et analytics
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import datetime

from backend.dependencies import get_current_user, get_db
from backend.services.analytics_service import AnalyticsService
from backend.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", status_code=status.HTTP_200_OK)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère les statistiques globales du dashboard

    Returns:
        dict: Statistiques parcelles, documents, utilisateurs avec tendances
    """
    try:
        analytics = AnalyticsService()
        # Passer une date de début pour la méthode get_usage_stats
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=30)  # Derniers 30 jours
        stats = analytics.get_usage_stats(start_date=start_date)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques: {str(e)}"
        )


@router.get("/summary", status_code=status.HTTP_200_OK)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère un résumé complet pour le dashboard
    
    Inclut: stats globales, parcelles par zone, documents par type, activité récente
    """
    try:
        analytics = AnalyticsService()
        summary = analytics.get_analytics_summary()
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du résumé: {str(e)}"
        )


@router.get("/activity", status_code=status.HTTP_200_OK)
def get_recent_activity(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère l'activité récente du système

    Args:
        limit: Nombre d'activités à retourner (1-100)
    """
    try:
        # Valider la limite pour éviter les abus
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La limite doit être comprise entre 1 et 100"
            )

        # Appel direct sans passer par AnalyticsService
        from backend.models.audit_log import AuditLog
        
        query = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
        logs = query.all()
        
        activities = []
        for log in logs:
            activities.append({
                'id': log.id,
                'action': log.action,
                'details': log.details,
                'timestamp': log.timestamp.isoformat() if log.timestamp else None,
                'user_id': log.user_id,
                'parcel_id': getattr(log, 'parcel_id', None)
            })
        
        return {
            'activities': activities,
            'total': len(activities)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_recent_activity: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'activité: {str(e)}"
        )


@router.get("/charts/parcels-by-zone", status_code=status.HTTP_200_OK)
def get_parcels_by_zone_chart(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Données pour graphique: Distribution des parcelles par zone
    """
    try:
        analytics = AnalyticsService()
        data = analytics.get_parcels_by_zone()
        return {
            'labels': [item['zone'] for item in data],
            'data': [item['count'] for item in data]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/charts/parcels-by-category", status_code=status.HTTP_200_OK)
def get_parcels_by_category_chart(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Données pour graphique: Distribution des parcelles par catégorie
    """
    try:
        analytics = AnalyticsService()
        data = analytics.get_parcels_by_category()
        return {
            'labels': [item['category'] for item in data],
            'data': [item['count'] for item in data]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/charts/documents-by-type", status_code=status.HTTP_200_OK)
def get_documents_by_type_chart(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Données pour graphique: Distribution des documents par type
    """
    try:
        analytics = AnalyticsService()
        data = analytics.get_documents_stats_by_type()
        return {
            'labels': [item['type'] for item in data],
            'data': [item['count'] for item in data],
            'sizes': [item['total_size'] for item in data]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/charts/time-series", status_code=status.HTTP_200_OK)
def get_time_series_chart(
    period: str = Query('30d', regex='^(7d|30d|90d|1y)$'),
    metric: str = Query('parcels', regex='^(parcels|documents)$'),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Données pour graphique: Évolution temporelle

    Args:
        period: Période ('7d', '30d', '90d', '1y')
        metric: Métrique ('parcels', 'documents')
    """
    try:
        # Valider les paramètres d'entrée pour éviter les injections
        valid_periods = {'7d': 7, '30d': 30, '90d': 90, '1y': 365}
        valid_metrics = {'parcels': 'parcels', 'documents': 'documents'}

        if period not in valid_periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: {list(valid_periods.keys())}"
            )

        if metric not in valid_metrics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Métrique invalide: {metric}. Valeurs valides: {list(valid_metrics.keys())}"
            )

        analytics = AnalyticsService(db)
        data = analytics.get_time_series_data(period=period, metric=metric)
        return {
            'dates': [item['date'] for item in data],
            'values': [item['count'] for item in data],
            'period': period,
            'metric': metric
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des données de série temporelle"
        )


@router.get("/top-zones", status_code=status.HTTP_200_OK)
def get_top_zones(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Top zones par nombre de parcelles

    Args:
        limit: Nombre de zones à retourner (1-20)
    """
    try:
        # Appel direct sans passer par AnalyticsService
        from sqlalchemy import func
        from backend.models.parcel import Parcel
        
        query = db.query(
            Parcel.zone,
            func.count(Parcel.id).label('parcel_count')
        ).filter(
            Parcel.zone.isnot(None),
            Parcel.zone != ''
        ).group_by(
            Parcel.zone
        ).order_by(
            func.count(Parcel.id).desc()
        ).limit(limit)
        
        results = query.all()
        
        zones = []
        for zone, count in results:
            zones.append({
                'name': zone,
                'parcel_count': count
            })
        
        return {
            'zones': zones,
            'total': len(zones)
        }
    except Exception as e:
        print(f"Error in get_top_zones: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des top zones: {str(e)}"
        )
