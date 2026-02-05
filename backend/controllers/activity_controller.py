"""
Activity Controller - API pour consulter les activités récentes
"""

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import datetime, timedelta

from backend.dependencies import get_current_user, get_db, require_admin
from backend.services.audit_service import AuditService
from backend.models.user import User

class ActivityController:
    """Contrôleur pour la gestion des activités du système"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/api", tags=["Activities"])
        self._register_routes()
    
    def _register_routes(self):
        """Enregistre les routes du contrôleur"""
        self.router.add_api_route("/activities", self.get_activities, methods=["GET"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/dashboard/activity", self.get_dashboard_activity, methods=["GET"], status_code=status.HTTP_200_OK)
        self.router.add_api_route("/users/{user_id}/activity", self.get_user_activity, methods=["GET"], status_code=status.HTTP_200_OK)
    
    def _get_icon_for_action(self, action: str) -> str:
        """Retourne l'icône Material Design correspondant à l'action"""
        icon_mapping = {
            'create': 'add_circle',
            'read': 'visibility',
            'update': 'edit',
            'modify': 'edit',
            'delete': 'delete',
            'login': 'login',
            'logout': 'logout',
            'export': 'download',
            'import': 'upload',
            'upload': 'cloud_upload',
            'download': 'cloud_download',
            'validate': 'check_circle',
            'assign': 'person_add',
            'parcel': 'location_on',
            'document': 'description',
            'user': 'person',
            'owner': 'person_pin',
            'alert': 'notifications',
            'system': 'settings'
        }
        return icon_mapping.get(action.lower(), 'info')

    def _get_color_for_action(self, action: str) -> str:
        """Retourne la couleur correspondant à l'action"""
        color_mapping = {
            'create': '#4CAF50',  # Vert
            'read': '#2196F3',   # Bleu
            'update': '#FF9800', # Orange
            'modify': '#FF9800', # Orange
            'delete': '#F44336', # Rouge
            'login': '#9C27B0',  # Violet
            'logout': '#607D8B', # Gris bleu
            'export': '#00BCD4', # Cyan
            'import': '#009688', # Vert foncé
            'upload': '#3F51B5', # Indigo
            'download': '#795548', # Marron
            'validate': '#8BC34A', # Vert clair
            'assign': '#E91E63'   # Rose
        }
        return color_mapping.get(action.lower(), '#607D8B')  # Gris par défaut

    async def get_activities(
        self,
        limit: int = Query(20, ge=1, le=100, description="Nombre d'activités à retourner"),
        sort: str = Query("timestamp", description="Champ de tri (timestamp, action, entity_type, etc.)"),
        order: str = Query("desc", description="Ordre de tri (asc, desc)"),
        action: Optional[str] = Query(None, description="Filtrer par type d'action"),
        entity_type: Optional[str] = Query(None, description="Filtrer par type d'entité"),
        user_id: Optional[str] = Query(None, description="Filtrer par utilisateur"),
        date_from: Optional[datetime] = Query(None, description="Date de début (ISO format)"),
        date_to: Optional[datetime] = Query(None, description="Date de fin (ISO format)"),
        current_user: User = Depends(get_current_user),
        db = Depends(get_db)
    ):
        """
        Récupère les activités récentes du système

        **Requires**: Authentication
        **Filters**: action, entity_type, user_id, dates
        """
        try:
            audit_service = AuditService(db)

            # Déterminer la direction de tri
            sort_desc = order.lower() == 'desc'

            # Récupérer les logs d'audit
            logs = audit_service.get_audit_logs(
                action=action,
                entity_type=entity_type,
                user_id=int(user_id) if user_id and user_id.isdigit() else None,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=0  # Pagination non prise en charge pour les activités récentes
            )

            # Trier les résultats selon les paramètres
            if sort == "timestamp":
                logs.sort(key=lambda x: x.get('timestamp', ''), reverse=sort_desc)
            elif sort == "action":
                logs.sort(key=lambda x: x.get('action', ''), reverse=sort_desc)
            elif sort == "entity_type":
                logs.sort(key=lambda x: x.get('entity_type', ''), reverse=sort_desc)
            elif sort == "username":
                logs.sort(key=lambda x: x.get('username', ''), reverse=sort_desc)

            # Limiter à la quantité demandée après tri
            logs = logs[:limit]

            # Mapper les logs d'audit aux activités attendues par l'interface Angular
            activities = []
            for log in logs:
                activity = {
                    'id': log.get('id'),
                    'title': f"{log.get('action_label', log.get('action', 'Action')).upper()} {log.get('entity_type', '').upper()}",
                    'description': f"{log.get('username', 'Utilisateur')} a {log.get('action_label', log.get('action', 'effectué une action'))} sur {log.get('entity_type', 'une entité')} #{log.get('entity_id', '')}",
                    'timestamp': log.get('timestamp'),
                    'icon': self._get_icon_for_action(log.get('action', '')),
                    'color': self._get_color_for_action(log.get('action', '')),
                    'userId': log.get('user_id'),
                    'userName': log.get('username', ''),
                    'action': log.get('action', ''),
                    'entityType': log.get('entity_type', ''),
                    'entityId': log.get('entity_id'),
                    # Champs additionnels pour la compatibilité avec l'affichage détaillé
                    'details': log.get('request_path', ''),
                    'status': log.get('status', ''),
                    'old_value': log.get('changes', {}).get('old', ''),
                    'new_value': log.get('changes', {}).get('new', ''),
                    'field': list(log.get('changes', {}).keys())[0] if log.get('changes') else '',
                    # Champs pour la compatibilité avec ActivityFeedComponent
                    'parcel_id': log.get('entity_id') if log.get('entity_type', '').lower() == 'parcel' else None,
                    'updated_by': log.get('user_id')
                }
                activities.append(activity)

            return {
                'activities': activities,
                'total': len(activities),
                'limit': limit,
                'filters': {
                    'action': action,
                    'entity_type': entity_type,
                    'user_id': user_id,
                    'date_from': date_from.isoformat() if date_from else None,
                    'date_to': date_to.isoformat() if date_to else None
                }
            }

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Paramètre utilisateur invalide"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la récupération des activités : {str(e)}"
            )

    async def get_dashboard_activity(
        self,
        limit: int = Query(20, ge=1, le=50, description="Nombre d'activités récentes"),
        current_user: User = Depends(get_current_user),
        db = Depends(get_db)
    ):
        """
        Récupère les activités récentes pour le dashboard

        **Requires**: Authentication
        """
        try:
            audit_service = AuditService(db)

            # Récupérer les logs d'audit récents
            logs = audit_service.get_audit_logs(
                limit=limit,
                offset=0
            )

            # Formatter les activités pour le dashboard
            activities = []
            for log in logs:
                # Mapper les données d'audit aux propriétés attendues par l'interface Angular
                activity = {
                    'id': log.get('id'),
                    'title': f"{log.get('action_label', log.get('action', 'Action')).upper()} {log.get('entity_type', '').upper()}",
                    'description': f"{log.get('username', 'Utilisateur')} a {log.get('action_label', log.get('action', 'effectué une action'))} sur {log.get('entity_type', 'une entité')} #{log.get('entity_id', '')}",
                    'timestamp': log.get('timestamp'),
                    'icon': self._get_icon_for_action(log.get('action', '')),
                    'color': self._get_color_for_action(log.get('action', '')),
                    'userId': log.get('user_id'),
                    'userName': log.get('username', ''),
                    'action': log.get('action', ''),
                    'entityType': log.get('entity_type', ''),
                    'entityId': log.get('entity_id'),
                    # Champs additionnels pour la compatibilité avec l'affichage détaillé
                    'details': log.get('request_path', ''),
                    'status': log.get('status', ''),
                    'old_value': log.get('changes', {}).get('old', ''),
                    'new_value': log.get('changes', {}).get('new', ''),
                    'field': list(log.get('changes', {}).keys())[0] if log.get('changes') else '',
                    # Champs pour la compatibilité avec ActivityFeedComponent
                    'parcel_id': log.get('entity_id') if log.get('entity_type', '').lower() == 'parcel' else None,
                    'updated_by': log.get('user_id')
                }
                activities.append(activity)

            return {
                'activities': activities,
                'count': len(activities)
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la récupération des activités du dashboard : {str(e)}"
            )

    async def get_user_activity(
        self,
        user_id: str,
        limit: int = Query(20, ge=1, le=100, description="Nombre d'activités à retourner"),
        current_user: User = Depends(get_current_user),
        db = Depends(get_db)
    ):
        """
        Récupère les activités d'un utilisateur spécifique

        **Requires**: Authentication
        """
        # Validation de l'ID utilisateur pour prévenir les injections
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, str(user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID utilisateur invalide"
            )

        try:
            audit_service = AuditService(db)

            # Récupérer les actions de l'utilisateur
            actions = audit_service.get_user_actions(
                user_id=user_id,
                limit=limit
            )

            # Formatter les activités selon le format attendu par l'interface Angular
            activities = []
            for action in actions:
                activity = {
                    'id': action.get('id'),
                    'title': f"{action.get('action_label', action.get('action', 'Action')).upper()} {action.get('entity_type', '').upper()}",
                    'description': f"Utilisateur a {action.get('action_label', action.get('action', 'effectué une action'))} sur {action.get('entity_type', 'une entité')} #{action.get('entity_id', '')}",
                    'timestamp': action.get('timestamp'),
                    'icon': self._get_icon_for_action(action.get('action', '')),
                    'color': self._get_color_for_action(action.get('action', '')),
                    'userId': action.get('user_id'),
                    'userName': action.get('username', ''),
                    'action': action.get('action', ''),
                    'entityType': action.get('entity_type', ''),
                    'entityId': action.get('entity_id'),
                    # Champs additionnels pour la compatibilité avec l'affichage détaillé
                    'details': action.get('request_path', ''),
                    'status': action.get('status', ''),
                    'old_value': action.get('changes', {}).get('old', ''),
                    'new_value': action.get('changes', {}).get('new', ''),
                    'field': list(action.get('changes', {}).keys())[0] if action.get('changes') else '',
                    'duration_ms': action.get('duration_ms'),
                    # Champs pour la compatibilité avec ActivityFeedComponent
                    'parcel_id': action.get('entity_id') if action.get('entity_type', '').lower() == 'parcel' else None,
                    'updated_by': action.get('user_id')
                }
                activities.append(activity)

            return {
                'activities': activities,
                'user_id': user_id,
                'count': len(activities)
            }

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID utilisateur invalide"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erreur lors de la récupération des activités de l'utilisateur : {str(e)}"
            )


# Créer une instance du contrôleur et exporter son routeur
activity_controller = ActivityController()
router = activity_controller.router