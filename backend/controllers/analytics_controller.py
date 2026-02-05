"""
Analytics Controller - API pour les analyses et statistiques
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pydantic import BaseModel

from sqlalchemy.orm import Session
from backend.dependencies import get_current_user, get_db, require_admin
from backend.services.analytics_service import AnalyticsService
from backend.models.user import User

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class TimeSeriesData(BaseModel):
    """Données pour les graphiques temporels"""
    labels: List[str]
    datasets: List[Dict[str, Any]]


class AnalyticsSummary(BaseModel):
    """Résumé des analyses"""
    total_parcels: int
    total_documents: int
    total_users: int
    new_parcels_today: int
    new_documents_today: int
    new_users_today: int
    activity_count_24h: int


@router.get("/timeseries", status_code=status.HTTP_200_OK)
def get_time_series_data(
    period: str = Query("30d", description="Période: 7d, 30d, 90d, 1y"),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les données de série temporelle pour les graphiques

    **Requires**: Admin role
    """
    try:
        # Validation de la période pour prévenir les injections
        import re
        if not re.match(r'^(7d|30d|90d|1y)$', period):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: 7d, 30d, 90d, 1y"
            )

        # Valider la période
        valid_periods = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
        if period not in valid_periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: {list(valid_periods.keys())}"
            )

        analytics_service = AnalyticsService(db)

        # Convertir la période en date de début
        now = datetime.utcnow()
        days = valid_periods[period]
        start_date = now - timedelta(days=days)

        data = analytics_service.get_time_series_data(start_date)

        return {
            "labels": data.get("labels", []),
            "datasets": data.get("datasets", []),
            "period": period,
            "generated_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des données de série temporelle : {str(e)}"
        )


@router.get("/summary", status_code=status.HTTP_200_OK)
def get_analytics_summary(
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère un résumé des analyses

    **Requires**: Admin role
    """
    try:
        analytics_service = AnalyticsService(db)
        summary = analytics_service.get_analytics_summary()
        
        return {
            "total_parcels": summary.get("total_parcels", 0),
            "total_documents": summary.get("total_documents", 0),
            "total_users": summary.get("total_users", 0),
            "new_parcels_today": summary.get("new_parcels_today", 0),
            "new_documents_today": summary.get("new_documents_today", 0),
            "new_users_today": summary.get("new_users_today", 0),
            "activity_count_24h": summary.get("activity_count_24h", 0),
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du résumé des analyses : {str(e)}"
        )


@router.get("/usage", status_code=status.HTTP_200_OK)
def get_usage_stats(
    period: str = Query("30d", description="Période: 7d, 30d, 90d, 1y"),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les statistiques d'utilisation

    **Requires**: Admin role
    """
    try:
        # Valider la période
        valid_periods = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
        if period not in valid_periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: {list(valid_periods.keys())}"
            )

        analytics_service = AnalyticsService(db)

        # Convertir la période en date de début
        now = datetime.utcnow()
        days = valid_periods[period]
        start_date = now - timedelta(days=days)

        usage_stats = analytics_service.get_usage_stats(start_date)

        return {
            **usage_stats,
            "period": period,
            "generated_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques d'utilisation : {str(e)}"
        )


@router.get("/user-engagement", status_code=status.HTTP_200_OK)
def get_user_engagement(
    period: str = Query("30d", description="Période: 7d, 30d, 90d, 1y"),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les statistiques d'engagement des utilisateurs

    **Requires**: Admin role
    """
    try:
        # Valider la période
        valid_periods = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}
        if period not in valid_periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: {list(valid_periods.keys())}"
            )

        analytics_service = AnalyticsService(db)

        # Convertir la période en date de début
        now = datetime.utcnow()
        days = valid_periods[period]
        start_date = now - timedelta(days=days)

        engagement_stats = analytics_service.get_user_engagement_stats(start_date)

        return {
            **engagement_stats,
            "period": period,
            "generated_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques d'engagement : {str(e)}"
        )


@router.get("/performance", status_code=status.HTTP_200_OK)
def get_performance_metrics(
    period: str = Query("7d", description="Période: 1d, 7d, 30d"),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les métriques de performance du système

    **Requires**: Admin role
    """
    try:
        # Valider la période
        valid_periods = {"1d": 1, "7d": 7, "30d": 30}
        if period not in valid_periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Période invalide: {period}. Valeurs valides: {list(valid_periods.keys())}"
            )

        analytics_service = AnalyticsService(db)

        # Convertir la période en date de début
        now = datetime.utcnow()
        days = valid_periods[period]
        start_date = now - timedelta(days=days)

        performance_metrics = analytics_service.get_performance_metrics(start_date)

        return {
            **performance_metrics,
            "period": period,
            "generated_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des métriques de performance : {str(e)}"
        )
@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard_analytics(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les analytics pour le dashboard
    """
    try:
        from backend.models.parcel import Parcel
        from backend.models.user import User as UserModel
        from backend.models.document import Document
        from backend.models.mutation import ParcelMutation
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Date du début du mois
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Statistiques de base
        total_parcels = db_session.query(Parcel).count()
        total_users = db_session.query(UserModel).count()
        total_documents = db_session.query(Document).count()
        
        # Nouvelles parcelles ce mois
        new_parcels_this_month = db_session.query(Parcel).filter(
            Parcel.created_at >= start_of_month
        ).count()
        
        # Mutations ce mois
        mutations_this_month = db_session.query(ParcelMutation).filter(
            ParcelMutation.created_at >= start_of_month
        ).count()
        
        # Documents uploadés ce mois
        documents_this_month = db_session.query(Document).filter(
            Document.uploaded_at >= start_of_month
        ).count()
        
        # Utilisateurs actifs (ayant créé des parcelles récemment)
        active_users = db_session.query(func.count(func.distinct(Parcel.created_by))).filter(
            Parcel.created_at >= datetime.now() - timedelta(days=30)
        ).scalar() or 0
        
        return {
            "totalParcels": total_parcels,
            "totalUsers": total_users,
            "totalDocuments": total_documents,
            "newParcelsThisMonth": new_parcels_this_month,
            "mutationsThisMonth": mutations_this_month,
            "documentsThisMonth": documents_this_month,
            "activeUsers": active_users,
            "lastUpdated": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/parcels-by-category", status_code=status.HTTP_200_OK)
def get_parcels_by_category(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Répartition des parcelles par catégorie"""
    try:
        from backend.models.parcel import Parcel
        from sqlalchemy import func
        
        results = db_session.query(
            Parcel.category,
            func.count(Parcel.id).label('count')
        ).group_by(Parcel.category).all()
        
        return {
            "labels": [r[0] or "Non défini" for r in results],
            "datasets": [{
                "label": "Parcelles",
                "data": [r[1] for r in results]
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/parcels-by-status", status_code=status.HTTP_200_OK)
def get_parcels_by_status(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Répartition des parcelles par statut"""
    try:
        from backend.models.parcel import Parcel
        from sqlalchemy import func
        
        results = db_session.query(
            Parcel.status,
            func.count(Parcel.id).label('count')
        ).group_by(Parcel.status).all()
        
        return {
            "labels": [r[0] or "available" for r in results],
            "datasets": [{
                "label": "Parcelles",
                "data": [r[1] for r in results]
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/parcels-by-zone", status_code=status.HTTP_200_OK)
def get_parcels_by_zone(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Répartition des parcelles par zone"""
    try:
        from backend.models.parcel import Parcel
        from sqlalchemy import func
        
        results = db_session.query(
            Parcel.zone,
            func.count(Parcel.id).label('count')
        ).group_by(Parcel.zone).limit(10).all()
        
        return {
            "labels": [r[0] or "Non défini" for r in results],
            "datasets": [{
                "label": "Parcelles",
                "data": [r[1] for r in results]
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/area-distribution", status_code=status.HTTP_200_OK)
def get_area_distribution(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Distribution des surfaces des parcelles"""
    try:
        from backend.models.parcel import Parcel
        from sqlalchemy import func, case
        
        # Créer des tranches de surface
        ranges = db_session.query(
            case(
                (Parcel.area < 100, '< 100 m²'),
                (Parcel.area < 500, '100-500 m²'),
                (Parcel.area < 1000, '500-1000 m²'),
                (Parcel.area < 5000, '1000-5000 m²'),
                else_='> 5000 m²'
            ).label('range'),
            func.count(Parcel.id).label('count')
        ).filter(Parcel.area.isnot(None)).group_by('range').all()
        
        return {
            "labels": [r[0] for r in ranges],
            "datasets": [{
                "label": "Parcelles",
                "data": [r[1] for r in ranges]
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-activity", status_code=status.HTTP_200_OK)
def get_recent_activity(
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activité récente (parcelles créées par jour)"""
    try:
        from backend.models.parcel import Parcel
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # 7 derniers jours
        start_date = datetime.now() - timedelta(days=7)
        
        results = db_session.query(
            func.date(Parcel.created_at).label('date'),
            func.count(Parcel.id).label('count')
        ).filter(
            Parcel.created_at >= start_date
        ).group_by(func.date(Parcel.created_at)).order_by('date').all()
        
        return {
            "labels": [str(r[0]) if r[0] else "N/A" for r in results],
            "datasets": [{
                "label": "Nouvelles parcelles",
                "data": [r[1] for r in results]
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
