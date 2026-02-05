"""
Service d'audit et traçabilité complet
Enregistre et recherche dans l'audit trail
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.core.repository_interfaces import IAuditLogRepository
from backend.models.audit_log import AuditLog


class AuditService:
    """Service pour la gestion de l'audit trail"""

    def __init__(self, audit_log_repository: IAuditLogRepository):
        self.audit_log_repository = audit_log_repository
    
    def log_action(
        self,
        action: str,
        entity_type: str,
        entity_id: str = None,
        user_id: str = None,
        username: str = None,
        user_role: str = None,
        old_data: dict = None,
        new_data: dict = None,
        user_ip: str = None,
        user_agent: str = None,
        request_method: str = None,
        request_path: str = None,
        duration_ms: int = None,
        status: str = "success",
        error_message: str = None,
        response_status: int = None,
        is_sensitive: bool = False,
        metadata: dict = None
    ) -> int:
        """
        Enregistre une action dans l'audit log

        Returns:
            int: ID du log créé
        """
        try:
            # Calculer le diff si old_data et new_data fournis
            changes = None
            if old_data and new_data:
                changes = self._calculate_diff(old_data, new_data)
            else:
                changes = None

            # Créer un objet AuditLog
            audit_log = AuditLog(
                action=action,
                entity_type=entity_type,
                entity_id=str(entity_id) if entity_id else None,
                user_id=user_id,
                username=username,
                user_role=user_role,
                old_data=old_data,
                new_data=new_data,
                changes=changes,
                user_ip=user_ip,
                user_agent=user_agent,
                request_method=request_method,
                request_path=request_path,
                duration_ms=duration_ms,
                status=status,
                error_message=error_message,
                response_status=response_status,
                is_sensitive=is_sensitive,
                metadata_ext=metadata,
                timestamp=datetime.now()
            )

            # Sauvegarder via le repository
            created_log = self.audit_log_repository.create(audit_log)

            # Retourner l'ID du log créé
            return created_log.id

        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'audit : {e}")
            return None
    
    def get_audit_logs(
        self,
        action: str = None,
        entity_type: str = None,
        entity_id: str = None,
        user_id: str = None,
        status: str = None,
        date_from: datetime = None,
        date_to: datetime = None,
        is_sensitive: bool = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Récupère les audit logs avec filtres

        Returns:
            list: Liste des audit logs
        """
        try:
            # Validation des paramètres pour prévenir les injections
            import re

            if action and (len(action) > 50 or not re.match(r'^[a-zA-Z0-9_\-\s]+$', action)):
                return []

            if entity_type and (len(entity_type) > 50 or not re.match(r'^[a-zA-Z0-9_]+$', entity_type)):
                return []

            if entity_id and (len(entity_id) > 100 or not re.match(r'^[a-zA-Z0-9_-]+$', entity_id)):
                return []

            if user_id and (len(user_id) > 100 or not re.match(r'^[a-zA-Z0-9_-]+$', user_id)):
                return []

            if status and (len(status) > 20 or not re.match(r'^[a-zA-Z]+$', status)):
                return []

            # Limiter les valeurs possibles pour éviter les attaques par déni de service
            if limit > 1000:
                limit = 1000
            if offset < 0:
                offset = 0

            # Appeler le repository pour récupérer les logs
            logs = self.audit_log_repository.get_audit_logs(
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                user_id=user_id,
                status=status,
                date_from=date_from,
                date_to=date_to,
                is_sensitive=is_sensitive,
                limit=limit,
                offset=offset
            )

            return logs

        except Exception as e:
            print(f"Erreur get_audit_logs : {e}")
            return []
    
    def get_entity_history(
        self,
        entity_type: str,
        entity_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Récupère l'historique complet d'une entité
        
        Args:
            entity_type: Type d'entité (parcel, user, etc.)
            entity_id: ID de l'entité
            limit: Nombre max de résultats
            
        Returns:
            list: Historique chronologique
        """
        return self.get_audit_logs(
            entity_type=entity_type,
            entity_id=entity_id,
            limit=limit
        )
    
    def get_user_actions(
        self,
        user_id: str,
        date_from: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Récupère toutes les actions d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            date_from: Date de début (optionnel)
            limit: Nombre max de résultats
            
        Returns:
            list: Actions de l'utilisateur
        """
        return self.get_audit_logs(
            user_id=user_id,
            date_from=date_from,
            limit=limit
        )
    
    def get_audit_stats(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        """
        Récupère des statistiques sur l'audit

        Returns:
            dict: Statistiques
        """
        try:
            # Appeler le repository pour récupérer les stats
            stats = self.audit_log_repository.get_audit_stats(
                date_from=date_from,
                date_to=date_to
            )
            return stats

        except Exception as e:
            print(f"Erreur get_audit_stats : {e}")
            return {}
    
    def search_audit_logs(
        self,
        search_term: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Recherche full-text dans les audit logs

        Args:
            search_term: Terme de recherche
            limit: Nombre max de résultats

        Returns:
            list: Logs correspondants
        """
        try:
            # Appeler le repository pour effectuer la recherche
            logs = self.audit_log_repository.search_audit_logs(
                search_term=search_term,
                limit=limit
            )
            return logs

        except Exception as e:
            print(f"Erreur search_audit_logs : {e}")
            return []
    
    def get_sensitive_actions(
        self,
        date_from: datetime = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Récupère les actions sensibles (suppressions, modifications critiques)

        Args:
            date_from: Date de début
            limit: Nombre max de résultats

        Returns:
            list: Actions sensibles
        """
        return self.get_audit_logs(
            is_sensitive=True,
            date_from=date_from,
            limit=limit
        )
    
    def get_action_statistics(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        """
        Récupère les statistiques détaillées par type d'action

        Returns:
            dict: Statistiques par action avec totaux et pourcentages
        """
        try:
            # Appeler le repository pour récupérer les stats
            stats = self.audit_log_repository.get_action_statistics(
                date_from=date_from,
                date_to=date_to
            )
            return stats

        except Exception as e:
            print(f"Erreur get_action_statistics : {e}")
            return {'total': 0, 'by_action': []}
    
    def get_top_users(
        self,
        date_from: datetime = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Récupère les utilisateurs les plus actifs

        Args:
            date_from: Date de début
            limit: Nombre d'utilisateurs

        Returns:
            list: Top utilisateurs avec nombre d'actions
        """
        try:
            # Appeler le repository pour récupérer les tops users
            top_users = self.audit_log_repository.get_top_users(
                date_from=date_from,
                limit=limit
            )
            return top_users

        except Exception as e:
            print(f"Erreur get_top_users : {e}")
            return []
    
    def _calculate_diff(self, old_data: dict, new_data: dict) -> dict:
        """
        Calcule le diff entre deux dictionnaires
        
        Returns:
            dict: Champs modifiés avec anciennes et nouvelles valeurs
        """
        changes = {}
        
        # Clés communes
        all_keys = set(old_data.keys()) | set(new_data.keys())
        
        for key in all_keys:
            old_value = old_data.get(key)
            new_value = new_data.get(key)
            
            if old_value != new_value:
                changes[key] = {
                    'old': old_value,
                    'new': new_value
                }
        
        return changes
    
    def cleanup_old_logs(self, days_to_keep: int = 365) -> int:
        """
        Supprime les logs anciens (rétention)

        Args:
            days_to_keep: Nombre de jours à conserver

        Returns:
            int: Nombre de logs supprimés
        """
        try:
            # Appeler le repository pour nettoyer les vieux logs
            deleted = self.audit_log_repository.cleanup_old_logs(
                days_to_keep=days_to_keep
            )
            return deleted

        except Exception as e:
            print(f"Erreur cleanup_old_logs : {e}")
            return 0
