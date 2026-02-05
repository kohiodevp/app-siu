"""
Report Controller - API pour la génération de rapports PDF et Excel
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from typing import Optional
from datetime import datetime
import io

from backend.dependencies import get_current_user, get_db, require_admin
from backend.services.report_service import ReportService
from backend.models.user import User

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/parcel/{parcel_id}/pdf", status_code=status.HTTP_200_OK)
def generate_parcel_report_pdf(
    parcel_id: str,
    include_history: bool = Query(True),
    include_documents: bool = Query(True),
    include_map: bool = Query(False),
    include_nearby: bool = Query(True),
    nearby_radius: float = Query(2.0, ge=0.1, le=10.0, description="Rayon de recherche pour les parcelles à proximité en km"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Génère un rapport PDF complet d'une parcelle

    **Requires**: Authentication
    **Includes**: Informations, historique, documents, carte (optionnel), parcelles à proximité (optionnel)
    """
    try:
        report_service = ReportService(db)
        
        pdf_bytes = report_service.generate_parcel_report_pdf(
            parcel_id=parcel_id,
            include_history=include_history,
            include_documents=include_documents,
            include_map=include_map,
            include_nearby=include_nearby,
            nearby_radius=nearby_radius
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=parcelle_{parcel_id}_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du rapport : {str(e)}"
        )


@router.get("/activity/pdf", status_code=status.HTTP_200_OK)
def generate_activity_report_pdf(
    days: int = Query(30, ge=1, le=365),
    user_id: Optional[int] = None,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Génère un rapport d'activité PDF
    
    **Requires**: Admin role
    **Period**: Derniers X jours
    """
    try:
        report_service = ReportService(db)
        
        pdf_bytes = report_service.generate_activity_report_pdf(
            days=days,
            user_id=user_id
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=activity_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du rapport : {str(e)}"
        )


@router.get("/export/parcels/excel", status_code=status.HTTP_200_OK)
def export_parcels_excel(
    zone: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Exporte les parcelles vers Excel avec formatage
    
    **Requires**: Authentication
    **Filters**: zone, status
    **Format**: XLSX avec feuilles multiples, graphiques, formules
    """
    try:
        report_service = ReportService(db)
        
        filters = {}
        if zone:
            filters['zone'] = zone
        if status_filter:
            filters['status'] = status_filter
        
        excel_bytes = report_service.export_parcels_excel(filters=filters)
        
        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=parcelles_export_{datetime.now().strftime('%Y%m%d')}.xlsx"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export Excel : {str(e)}"
        )


@router.get("/export/documents/excel", status_code=status.HTTP_200_OK)
def export_documents_excel(
    parcel_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Exporte les documents vers Excel

    **Requires**: Authentication
    **Filter**: parcel_id (optionnel)
    """
    try:
        report_service = ReportService(db)

        # Valider l'ID de parcelle s'il est fourni
        if parcel_id:
            import re
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(uuid_pattern, str(parcel_id)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID de parcelle invalide"
                )

        excel_bytes = report_service.export_documents_excel(parcel_id=parcel_id)

        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=documents_export_{datetime.now().strftime('%Y%m%d')}.xlsx"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export Excel : {str(e)}"
        )


@router.get("/audit/pdf", status_code=status.HTTP_200_OK)
def generate_audit_report_pdf(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Génère un rapport d'audit PDF complet
    
    **Requires**: Admin role
    **Includes**: 
    - Vue d'ensemble avec statistiques globales
    - Top 10 utilisateurs actifs
    - Répartition des actions par type
    - Actions sensibles et critiques
    - Analyse par type d'entité
    - Historique des actions récentes
    - Recommandations de sécurité
    """
    try:
        report_service = ReportService(db)
        pdf_bytes = report_service.generate_audit_report_pdf(days=days)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=audit_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history", status_code=status.HTTP_200_OK)
def get_report_history(
    user_id: Optional[str] = None,
    limit: int = 50,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère l'historique des rapports générés.
    
    Query params:
        user_id: Filtrer par utilisateur (optionnel)
        limit: Nombre maximum de rapports
    """
    
    report_service = ReportService(db)
    history = report_service.get_report_history(user_id, limit)
    
    return {
        "success": True,
        "count": len(history),
        "reports": history
    }


@router.get("/templates", status_code=status.HTTP_200_OK)
def get_report_templates(
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les modèles de rapports disponibles.
    """
    
    report_service = ReportService(db)
    templates = report_service.get_report_templates()
    
    return {
        "success": True,
        "templates": templates
    }


@router.post("/schedule", status_code=status.HTTP_201_CREATED)
def schedule_report(
    report_type: str,
    parameters: dict,
    schedule_type: str,
    schedule_time: str,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Planifie la génération automatique d'un rapport.
    
    Body:
        report_type: Type de rapport
        parameters: Paramètres du rapport
        schedule_type: daily, weekly, monthly
        schedule_time: Heure au format HH:MM
    """
    
    report_service = ReportService(db)
    
    result = report_service.schedule_report(
        report_type=report_type,
        user_id=current_user.id,
        parameters=parameters,
        schedule_type=schedule_type,
        schedule_time=schedule_time
    )
    
    return {
        "success": True,
        "message": "Report scheduled successfully",
        "schedule": result
    }


@router.post("/export/excel", status_code=status.HTTP_200_OK)
def export_data_excel(
    filters: dict = None,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Exporte des données vers Excel selon les filtres spécifiés

    **Requires**: Admin role
    """
    try:
        
        report_service = ReportService(db)

        excel_bytes = report_service.export_filtered_data_excel(filters=filters or {})

        

        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export Excel : {str(e)}"
        )


@router.post("/export/csv", status_code=status.HTTP_200_OK)
def export_data_csv(
    filters: dict = None,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Exporte des données vers CSV selon les filtres spécifiés

    **Requires**: Admin role
    """
    try:
        
        report_service = ReportService(db)

        csv_bytes = report_service.export_filtered_data_csv(filters=filters or {})

        

        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export CSV : {str(e)}"
        )


@router.post("/export/geojson", status_code=status.HTTP_200_OK)
def export_geojson(
    filters: dict = None,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Exporte les données géospatiales vers GeoJSON selon les filtres spécifiés

    **Requires**: Admin role
    """
    try:
        
        report_service = ReportService(db)

        geojson_data = report_service.export_filtered_data_geojson(filters=filters or {})

        

        return StreamingResponse(
            io.BytesIO(geojson_data.encode()),
            media_type="application/geo+json",
            headers={
                "Content-Disposition": f"attachment; filename=geo_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.geojson"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export GeoJSON : {str(e)}"
        )


@router.post("/export/pdf", status_code=status.HTTP_200_OK)
def export_data_pdf(
    filters: dict = None,
    db = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Exporte des données vers PDF selon les filtres spécifiés

    **Requires**: Admin role
    """
    try:
        
        report_service = ReportService(db)

        pdf_bytes = report_service.export_filtered_data_pdf(filters=filters or {})

        

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export PDF : {str(e)}"
        )
