"""
Endpoints pour les fonctionnalités avancées de recherche
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from backend.dependencies import get_db, get_current_user
from backend.models.user import User
from backend.services.search_service import SearchService
from backend.services.analytics_service import AnalyticsService
from backend.services.workflow_service import WorkflowService
from backend.services.document_service import DocumentService
from backend.services.mutation_service import MutationService

router = APIRouter(prefix="/api/advanced", tags=["Advanced Features"])

@router.get("/search")
def advanced_search(
    query: str = Query(..., min_length=1),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    min_area: Optional[float] = Query(None),
    max_area: Optional[float] = Query(None),
    coordinates: Optional[str] = Query(None),  # format: "lat,lng"
    radius_km: Optional[float] = Query(None, ge=0.1, le=50.0),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche avancée avec tous les critères possibles
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    filters = {
        'query': query,
        'category': category,
        'status': status,
        'zone': zone,
        'min_area': min_area,
        'max_area': max_area,
        'page': page,
        'page_size': page_size
    }
    
    if coordinates and radius_km:
        try:
            lat, lng = map(float, coordinates.split(','))
            filters['coordinates'] = {'lat': lat, 'lng': lng}
            filters['radius_km'] = radius_km
        except ValueError:
            raise HTTPException(status_code=400, detail="Coordonnées invalides. Format attendu: lat,lng")
    
    results = search_service.advanced_search(filters)
    return results


@router.get("/geocode")
def geocode_address(
    address: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Géocode une adresse vers des coordonnées
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    try:
        results = search_service.geocode_address(address)
        return {"results": results, "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de géocodage: {str(e)}")


@router.get("/reverse-geocode")
def reverse_geocode(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Géocode inversé - coordonnées vers adresse
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    try:
        result = search_service.reverse_geocode(lat, lng)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de géocodage inverse: {str(e)}")


@router.get("/nearby")
def search_nearby(
    lat: float,
    lng: float,
    radius_km: float = Query(1.0, ge=0.1, le=50.0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche les parcelles à proximité d'un point
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    try:
        results = search_service.search_nearby(lat, lng, radius_km, limit)
        # Filtrer par catégorie et statut si spécifiés
        if category:
            results = [r for r in results if r.get('category') == category]
        if status:
            results = [r for r in results if r.get('status') == status]
        
        return {
            "results": results[:limit],
            "total": len(results),
            "center": {"lat": lat, "lng": lng},
            "radius_km": radius_km
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche à proximité: {str(e)}")


@router.post("/within-geometry")
def search_within_geometry(
    geometry: Dict[str, Any],
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche les parcelles à l'intérieur d'une géométrie
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    try:
        results = search_service.search_within_geometry(
            geometry=geometry.get('coordinates', []),
            category=category,
            status=status
        )
        return {
            "results": results[:limit],
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche dans la géométrie: {str(e)}")


@router.post("/intersect-geometry")
def search_intersect_geometry(
    geometry: Dict[str, Any],
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche les parcelles qui intersectent une géométrie
    """
    from backend.container_config import get_search_service
    search_service = get_search_service()
    
    try:
        results = search_service.search_intersecting(
            geometry=geometry.get('coordinates', []),
            category=category,
            status=status
        )
        return {
            "results": results[:limit],
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche d'intersection: {str(e)}")


@router.get("/analytics/dashboard-stats")
def get_dashboard_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    localite: Optional[str] = Query(None),
    commune: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques du tableau de bord
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status,
        'region': region,
        'province': province,
        'localite': localite,
        'commune': commune
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    stats = analytics_service.get_dashboard_stats(filters)
    return stats


@router.get("/analytics/parcels-by-category")
def get_parcels_by_category(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les données pour le graphique des parcelles par catégorie
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['endDate'] = end_date
    if zone: filters['zone'] = zone
    if status: filters['status'] = status
    
    chart_data = analytics_service.get_parcels_by_category(filters)
    return chart_data


@router.get("/analytics/parcels-by-status")
def get_parcels_by_status(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les données pour le graphique des parcelles par statut
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['endDate'] = end_date
    if category: filters['category'] = category
    if zone: filters['zone'] = zone
    
    chart_data = analytics_service.get_parcels_by_status(filters)
    return chart_data


@router.get("/analytics/parcels-by-zone")
def get_parcels_by_zone(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les données pour le graphique des parcelles par zone
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['endDate'] = end_date
    if category: filters['category'] = category
    if status: filters['status'] = status
    
    chart_data = analytics_service.get_parcels_by_zone(filters)
    return chart_data


@router.get("/analytics/area-distribution")
def get_area_distribution(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les données pour le graphique de distribution des surfaces
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['endDate'] = end_date
    if category: filters['category'] = category
    if zone: filters['zone'] = zone
    if status: filters['status'] = status
    
    chart_data = analytics_service.get_area_distribution(filters)
    return chart_data


@router.get("/analytics/recent-activity")
def get_recent_activity(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les données pour le graphique des activités récentes
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['EndDate'] = end_date
    if category: filters['category'] = category
    if zone: filters['zone'] = zone
    
    chart_data = analytics_service.get_recent_activity(filters)
    return chart_data


@router.post("/reports/{report_type}/pdf")
def generate_pdf_report(
    report_type: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    localite: Optional[str] = Query(None),
    commune: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génère un rapport PDF
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status,
        'region': region,
        'province': province,
        'localite': localite,
        'commune': commune
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        report_blob = analytics_service.generate_pdf_report(report_type, filters)
        return report_blob
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération du rapport PDF: {str(e)}")


@router.post("/reports/{report_type}/excel")
def generate_excel_report(
    report_type: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    localite: Optional[str] = Query(None),
    commune: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génère un rapport Excel
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status,
        'region': region,
        'province': province,
        'localite': localite,
        'commune': commune
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        report_blob = analytics_service.generate_excel_report(report_type, filters)
        return report_blob
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération du rapport Excel: {str(e)}")


@router.post("/reports/{report_type}/csv")
def generate_csv_report(
    report_type: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    localite: Optional[str] = Query(None),
    commune: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génère un rapport CSV
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status,
        'region': region,
        'province': province,
        'localite': localite,
        'commune': commune
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        report_blob = analytics_service.generate_csv_report(report_type, filters)
        return report_blob
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération du rapport CSV: {str(e)}")


@router.get("/reports/history")
def get_report_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère l'historique des rapports
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    history = analytics_service.get_report_history(page, page_size)
    return history


@router.get("/workflows/pending")
def get_pending_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les workflows en attente pour l'utilisateur
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    workflows = workflow_service.get_pending_workflows(current_user.id)
    return {"workflows": workflows, "total": len(workflows)}


@router.get("/workflows/initiated")
def get_initiated_workflows(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les workflows initiés par l'utilisateur
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    workflows = workflow_service.get_user_workflows(current_user.id, status)
    return {
        "workflows": workflows[(page-1)*page_size:page*page_size],
        "total": len(workflows),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(workflows) + page_size - 1) // page_size
    }


@router.get("/workflows/type/{workflow_type}")
def get_workflows_by_type(
    workflow_type: str,
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les workflows par type
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    workflows = workflow_service.get_workflows_by_type(workflow_type, status)
    return {
        "workflows": workflows[(page-1)*page_size:page*page_size],
        "total": len(workflows),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(workflows) + page_size - 1) // page_size
    }


@router.post("/workflows/{workflow_id}/approval")
def submit_approval(
    workflow_id: str,
    action: str = Query(..., regex="^(approve|reject|comment)$"),
    comment: Optional[str] = Query(None),
    step_id: Optional[str] = Query(None),
    attachment_ids: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Soumet une approbation pour une étape de workflow
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    approval_request = {
        'workflow_id': workflow_id,
        'step_id': step_id or '',
        'approver_id': current_user.id,
        'action': action,
        'comment': comment or '',
        'attachments': attachment_ids or []
    }
    
    try:
        result = workflow_service.submit_approval(approval_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de soumission de l'approbation: {str(e)}")


@router.post("/workflows/{workflow_id}/comment")
def add_comment_to_workflow(
    workflow_id: str,
    step_id: str,
    comment: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ajoute un commentaire à une étape de workflow
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    try:
        result = workflow_service.add_comment(workflow_id, step_id, comment)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'ajout du commentaire: {str(e)}")


@router.put("/workflows/{workflow_id}/cancel")
def cancel_workflow(
    workflow_id: str,
    reason: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Annule un workflow
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    try:
        result = workflow_service.cancel_workflow(workflow_id, reason)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'annulation du workflow: {str(e)}")


@router.get("/workflows/approvers/{workflow_type}")
def get_possible_approvers(
    workflow_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les approbateurs possibles pour un type de workflow
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    try:
        approvers = workflow_service.get_possible_approvers(workflow_type)
        return {"approvers": approvers, "total": len(approvers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des approbateurs: {str(e)}")


@router.get("/workflows/stats")
def get_workflow_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques des workflows
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    try:
        stats = workflow_service.get_workflow_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des statistiques: {str(e)}")


@router.get("/workflows/history")
def get_workflow_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    workflow_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    initiated_by: Optional[str] = Query(None),
    entity_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère l'historique des workflows
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    filters = {}
    if workflow_type: filters['type'] = workflow_type
    if status: filters['status'] = status
    if initiated_by: filters['initiated_by'] = initiated_by
    if entity_id: filters['entity_id'] = entity_id
    
    try:
        history = workflow_service.get_workflow_history(page, page_size, filters)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération de l'historique: {str(e)}")


@router.get("/workflows/overdue")
def get_overdue_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les workflows en retard
    """
    from backend.container_config import get_workflow_service
    workflow_service = get_workflow_service()
    
    try:
        workflows = workflow_service.get_overdue_workflows()
        return {"workflows": workflows, "total": len(workflows)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des workflows en retard: {str(e)}")


@router.get("/mutations/pending-legal-validation")
def get_mutations_pending_legal_validation(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les mutations en attente de validation juridique
    """
    from backend.container_config import get_mutation_service
    mutation_service = get_mutation_service()
    
    try:
        mutations = mutation_service.get_mutations_pending_legal_validation(page, page_size)
        return mutations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des mutations en attente de validation juridique: {str(e)}")


@router.get("/mutations/pending-technical-validation")
def get_mutations_pending_technical_validation(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les mutations en attente de validation technique
    """
    from backend.container_config import get_mutation_service
    mutation_service = get_mutation_service()
    
    try:
        mutations = mutation_service.get_mutations_pending_technical_validation(page, page_size)
        return mutations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des mutations en attente de validation technique: {str(e)}")


@router.get("/mutations/pending-administrative-validation")
def get_mutations_pending_administrative_validation(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les mutations en attente de validation administrative
    """
    from backend.container_config import get_mutation_service
    mutation_service = get_mutation_service()
    
    try:
        mutations = mutation_service.get_mutations_pending_administrative_validation(page, page_size)
        return mutations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des mutations en attente de validation administrative: {str(e)}")


@router.get("/documents/search-text")
def search_documents_by_text(
    query: str = Query(..., min_length=1),
    parcel_id: Optional[str] = Query(None),
    document_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche dans le texte des documents
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        results = document_service.search_in_documents(query, parcel_id, document_type, page, page_size)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche dans les documents: {str(e)}")


@router.get("/documents/{document_id}/preview")
def get_document_preview(
    document_id: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génère un aperçu d'un document
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        preview = document_service.generate_preview(document_id, page)
        return preview
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération de l'aperçu: {str(e)}")


@router.get("/documents/{document_id}/thumbnail")
def get_document_thumbnail(
    document_id: str,
    width: int = Query(200, ge=50, le=1000),
    height: int = Query(200, ge=50, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génère une miniature d'un document
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        thumbnail = document_service.generate_thumbnail(document_id, width, height)
        return thumbnail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération de la miniature: {str(e)}")


@router.post("/documents/{document_id}/ocr")
def extract_text_from_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Extrait le texte d'un document (OCR)
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        text_data = document_service.extract_text(document_id)
        return text_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'extraction du texte: {str(e)}")


@router.get("/documents/{document_id}/analyze")
def analyze_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyse un document pour extraction d'informations
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        analysis = document_service.analyze_document(document_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse du document: {str(e)}")


@router.get("/documents/popular-tags")
def get_popular_tags(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les tags les plus populaires
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        tags = document_service.get_popular_tags(limit)
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des tags populaires: {str(e)}")


@router.get("/documents/search-tags")
def search_documents_by_tags(
    tags: List[str] = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recherche des documents par tags
    """
    from backend.container_config import get_document_service
    document_service = get_document_service()
    
    try:
        results = document_service.search_by_tags(tags, page, page_size)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de recherche par tags: {str(e)}")


@router.get("/analytics/geographic-trends")
def get_geographic_trends(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les tendances géographiques
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['endDate'] = end_date
    if category: filters['category'] = category
    if status: filters['status'] = status
    
    try:
        trends = analytics_service.get_geographic_trends(filters)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des tendances géographiques: {str(e)}")


@router.get("/analytics/performance")
def get_performance_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques de performance
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['EndDate'] = end_date
    
    try:
        stats = analytics_service.get_performance_stats(filters)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des statistiques de performance: {str(e)}")


@router.get("/analytics/alerts")
def get_alerts_and_anomalies(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les alertes et anomalies
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['EndDate'] = end_date
    if category: filters['category'] = category
    if zone: filters['zone'] = zone
    
    try:
        alerts = analytics_service.get_alerts_and_anomalies(filters)
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des alertes: {str(e)}")


@router.get("/analytics/predictions")
def get_predictions(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les prédictions et analyses
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {}
    if start_date: filters['startDate'] = start_date
    if end_date: filters['EndDate'] = end_date
    if category: filters['category'] = category
    if zone: filters['zone'] = zone
    
    try:
        predictions = analytics_service.getPredictions(filters)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des prédictions: {str(e)}")


@router.post("/analytics/export-raw")
def export_raw_data(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    localite: Optional[str] = Query(None),
    commune: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Exporte les données brutes
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status,
        'region': region,
        'province': province,
        'localite': localite,
        'commune': commune
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        raw_data = analytics_service.export_raw_data(filters)
        return raw_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'export des données brutes: {str(e)}")


@router.get("/analytics/stats-by-period")
def get_stats_by_period(
    period: str = Query(..., regex="^(daily|weekly|monthly|quarterly|yearly)$"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques par période
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        stats = analytics_service.get_stats_by_period(period, filters)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des statistiques par période: {str(e)}")


@router.get("/analytics/comparisons")
def get_comparisons(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les comparaisons
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'endDate': end_date,
        'category': category,
        'zone': zone,
        'status': status
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        comparisons = analytics_service.get_comparisons(filters)
        return comparisons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des comparaisons: {str(e)}")


@router.get("/analytics/owners-distribution")
def get_owners_distribution(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la distribution des propriétaires
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'EndDate': end_date,
        'category': category,
        'zone': zone
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        distribution = analytics_service.get_owners_distribution(filters)
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération de la distribution des propriétaires: {str(e)}")


@router.get("/analytics/documents-distribution")
def get_documents_distribution(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la distribution des documents
    """
    from backend.container_config import get_analytics_service
    analytics_service = get_analytics_service()
    
    filters = {
        'startDate': start_date,
        'EndDate': end_date,
        'category': category,
        'zone': zone
    }
    
    # Supprimer les valeurs None
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        distribution = analytics_service.get_documents_distribution(filters)
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération de la distribution des documents: {str(e)}")