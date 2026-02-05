"""
Audit Controller - API pour consulter l'audit trail
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from typing import Optional
from datetime import datetime, timedelta
import csv
import io
import json

from backend.dependencies import get_current_user, get_db, require_admin
from backend.services.audit_service import AuditService
from backend.models.user import User

router = APIRouter(prefix="/api/audit", tags=["Audit"])


@router.get("/logs", status_code=status.HTTP_200_OK)
def get_audit_logs(
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    user_id: Optional[int] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    is_sensitive: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère les audit logs avec filtres

    **Requires**: Admin role
    **Filters**: action, entity_type, entity_id, user_id, status, dates, is_sensitive
    """
    try:
        # Validation des paramètres pour prévenir les injections
        if action and (len(action) > 50 or not re.match(r'^[a-zA-Z0-9_\-\s]+$', action)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action invalide"
            )

        if entity_type and (len(entity_type) > 50 or not re.match(r'^[a-zA-Z0-9_]+$', entity_type)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entity type invalide"
            )

        if entity_id and (len(entity_id) > 100 or not re.match(r'^[a-zA-Z0-9_-]+$', entity_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entity ID invalide"
            )

        if status_filter and (len(status_filter) > 20 or not re.match(r'^[a-zA-Z]+$', status_filter)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status invalide"
            )

        audit_service = AuditService(db)

        logs = audit_service.get_audit_logs(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            status=status_filter,
            date_from=date_from,
            date_to=date_to,
            is_sensitive=is_sensitive,
            limit=limit,
            offset=offset
        )

        return {
            'logs': logs,
            'total': len(logs),
            'limit': limit,
            'offset': offset
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des logs : {str(e)}"
        )


@router.get("/entity/{entity_type}/{entity_id}", status_code=status.HTTP_200_OK)
def get_entity_history(
    entity_type: str,
    entity_id: str,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Récupère l'historique complet d'une entité

    **Requires**: Authentication
    **Returns**: Historique chronologique des modifications
    """
    try:
        # Validation des paramètres pour prévenir les injections
        if len(entity_type) > 50 or not re.match(r'^[a-zA-Z0-9_]+$', entity_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entity type invalide"
            )

        if len(entity_id) > 100 or not re.match(r'^[a-zA-Z0-9_-]+$', entity_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entity ID invalide"
            )

        audit_service = AuditService(db)
        history = audit_service.get_entity_history(
            entity_type=entity_type,
            entity_id=entity_id,
            limit=limit
        )

        return {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'history': history,
            'total': len(history)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user_actions(
    user_id: str,
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère toutes les actions d'un utilisateur

    **Requires**: Admin role
    **Args**: days = nombre de jours à remonter
    """
    try:
        # Validation de l'ID utilisateur pour prévenir les injections
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, str(user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID utilisateur invalide"
            )

        date_from = datetime.utcnow() - timedelta(days=days)

        audit_service = AuditService(db)
        actions = audit_service.get_user_actions(
            user_id=user_id,
            date_from=date_from,
            limit=limit
        )

        return {
            'user_id': user_id,
            'period_days': days,
            'actions': actions,
            'total': len(actions)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/stats", status_code=status.HTTP_200_OK)
def get_audit_stats(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Récupère des statistiques sur l'audit
    
    **Requires**: Admin role
    **Returns**: Statistiques globales, par action, par entité, top users
    """
    try:
        date_from = datetime.utcnow() - timedelta(days=days)
        
        audit_service = AuditService(db)
        stats = audit_service.get_audit_stats(
            date_from=date_from,
            date_to=datetime.utcnow()
        )
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/search", status_code=status.HTTP_200_OK)
def search_audit_logs(
    q: str = Query(..., min_length=2),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Recherche full-text dans les audit logs

    **Requires**: Admin role
    **Search in**: username, request_path, entity_id, error_message
    """
    try:
        # Validation du terme de recherche pour prévenir les injections
        if len(q) > 100 or not re.match(r'^[a-zA-Z0-9\s\-\._@]+$', q):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Terme de recherche invalide"
            )

        audit_service = AuditService(db)
        results = audit_service.search_audit_logs(
            search_term=q,
            limit=limit
        )

        return {
            'query': q,
            'results': results,
            'total': len(results)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/export/csv", status_code=status.HTTP_200_OK)
def export_audit_logs_csv(
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Exporte les audit logs en CSV
    
    **Requires**: Admin role
    **Format**: CSV avec tous les champs
    """
    try:
        date_from = datetime.utcnow() - timedelta(days=days)
        
        audit_service = AuditService(db)
        logs = audit_service.get_audit_logs(
            date_from=date_from,
            limit=10000  # Maximum pour export
        )
        
        # Créer CSV en mémoire
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'id', 'timestamp', 'action', 'entity_type', 'entity_id',
                'user_id', 'username', 'user_role', 'user_ip',
                'request_method', 'request_path', 'status',
                'duration_ms', 'response_status'
            ]
        )
        
        writer.writeheader()
        for log in logs:
            writer.writerow({
                'id': log['id'],
                'timestamp': log['timestamp'],
                'action': log['action'],
                'entity_type': log['entity_type'],
                'entity_id': log['entity_id'],
                'user_id': log['user_id'],
                'username': log['username'],
                'user_role': log['user_role'],
                'user_ip': log['user_ip'],
                'request_method': log['request_method'],
                'request_path': log['request_path'],
                'status': log['status'],
                'duration_ms': log['duration_ms'],
                'response_status': log['response_status']
            })
        
        # Retourner comme fichier téléchargeable
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=audit_logs_{datetime.utcnow().strftime('%Y%m%d')}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/export/json", status_code=status.HTTP_200_OK)
def export_audit_logs_json(
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Exporte les audit logs en JSON
    
    **Requires**: Admin role
    **Format**: JSON complet avec tous les détails
    """
    try:
        date_from = datetime.utcnow() - timedelta(days=days)
        
        audit_service = AuditService(db)
        logs = audit_service.get_audit_logs(
            date_from=date_from,
            limit=10000
        )
        
        # Créer JSON
        export_data = {
            'export_date': datetime.utcnow().isoformat(),
            'period_days': days,
            'total_logs': len(logs),
            'logs': logs
        }
        
        json_str = json.dumps(export_data, indent=2, default=str)
        
        return StreamingResponse(
            iter([json_str]),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=audit_logs_{datetime.utcnow().strftime('%Y%m%d')}.json"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/cleanup", status_code=status.HTTP_200_OK)
def cleanup_old_logs(
    days_to_keep: int = Query(365, ge=30, le=3650),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Supprime les logs anciens (politique de rétention)
    
    **Requires**: Admin role
    **Warning**: Action irréversible
    **Note**: Les logs sensibles sont toujours conservés
    """
    try:
        audit_service = AuditService(db)
        deleted_count = audit_service.cleanup_old_logs(days_to_keep=days_to_keep)
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'days_kept': days_to_keep,
            'message': f'{deleted_count} logs supprimés (> {days_to_keep} jours)'
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
