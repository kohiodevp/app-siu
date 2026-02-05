"""
Implémentation du repository pour les logs d'audit.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_, exc as sql_exceptions

from backend.core.repository_interfaces import IAuditLogRepository
from backend.models.audit_log import AuditLog


class SqlAuditLogRepository(IAuditLogRepository):
    """
    Implémentation SQLAlchemy du repository des logs d'audit.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: str) -> Optional[AuditLog]:
        try:
            return self.db_session.query(AuditLog).filter(AuditLog.id == id).first()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération du log d'audit par ID: {e}")
            return None

    def get_all(self) -> List[AuditLog]:
        try:
            return self.db_session.query(AuditLog).all()
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de tous les logs d'audit: {e}")
            return []

    def create(self, entity: AuditLog) -> AuditLog:
        try:
            self.db_session.add(entity)
            self.db_session.flush()
            return entity
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors de la création du log d'audit: {e}")
            raise e

    def update(self, id: str, entity: AuditLog) -> Optional[AuditLog]:
        return None  # Les logs sont immuables

    def delete(self, id: str) -> bool:
        return False  # Les logs ne sont pas supprimés

    def search(self, criteria: Dict[str, Any]) -> List[AuditLog]:
        try:
            return []
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des logs d'audit: {e}")
            return []

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
        try:
            query = self.db_session.query(AuditLog)

            if action:
                query = query.filter(AuditLog.action == action)
            if entity_type:
                query = query.filter(AuditLog.entity_type == entity_type)
            if entity_id:
                query = query.filter(AuditLog.entity_id == str(entity_id))
            if user_id:
                query = query.filter(AuditLog.user_id == user_id)
            if status:
                query = query.filter(AuditLog.status == status)
            if date_from:
                query = query.filter(AuditLog.timestamp >= date_from)
            if date_to:
                query = query.filter(AuditLog.timestamp <= date_to)
            if is_sensitive is not None:
                query = query.filter(AuditLog.is_sensitive == is_sensitive)

            query = query.order_by(AuditLog.timestamp.desc())
            query = query.offset(offset).limit(limit)

            rows = query.all()
            logs = []
            for row in rows:
                log_dict = {
                    'id': row.id,
                    'action': row.action,
                    'entity_type': row.entity_type,
                    'entity_id': row.entity_id,
                    'user_id': row.user_id,
                    'username': row.username,
                    'user_role': row.user_role,
                    'old_data': json.loads(row.old_data) if row.old_data else None,
                    'new_data': json.loads(row.new_data) if row.new_data else None,
                    'changes': json.loads(row.changes) if row.changes else None,
                    'user_ip': row.user_ip,
                    'user_agent': row.user_agent,
                    'request_method': row.request_method,
                    'request_path': row.request_path,
                    'duration_ms': row.duration_ms,
                    'status': row.status,
                    'error_message': row.error_message,
                    'response_status': row.response_status,
                    'is_sensitive': bool(row.is_sensitive),
                    'timestamp': row.timestamp.isoformat() if hasattr(row.timestamp, 'isoformat') else str(row.timestamp),
                    'metadata_ext': json.loads(row.metadata_ext) if row.metadata_ext else None
                }
                logs.append(log_dict)
            return logs
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des logs d'audit: {e}")
            return []

    def get_entity_history(
        self,
        entity_type: str,
        entity_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            return self.get_audit_logs(
                entity_type=entity_type,
                entity_id=entity_id,
                limit=limit
            )
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération de l'historique de l'entité: {e}")
            return []

    def get_user_actions(
        self,
        user_id: str,
        date_from: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            return self.get_audit_logs(
                user_id=user_id,
                date_from=date_from,
                limit=limit
            )
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des actions de l'utilisateur: {e}")
            return []

    def get_audit_stats(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        try:
            query = self.db_session.query(AuditLog)

            if date_from:
                query = query.filter(AuditLog.timestamp >= date_from)
            if date_to:
                query = query.filter(AuditLog.timestamp <= date_to)

            total = query.count()

            by_action = dict(
                self.db_session.query(AuditLog.action, func.count(AuditLog.id))
                .filter(AuditLog.timestamp >= date_from) if date_from else AuditLog.action
                .filter(AuditLog.timestamp <= date_to) if date_to else AuditLog.action
                .group_by(AuditLog.action)
                .all()
            )

            by_entity = dict(
                self.db_session.query(AuditLog.entity_type, func.count(AuditLog.id))
                .filter(AuditLog.timestamp >= date_from) if date_from else AuditLog.entity_type
                .filter(AuditLog.timestamp <= date_to) if date_to else AuditLog.entity_type
                .group_by(AuditLog.entity_type)
                .all()
            )

            by_status = dict(
                self.db_session.query(AuditLog.status, func.count(AuditLog.id))
                .filter(AuditLog.timestamp >= date_from) if date_from else AuditLog.status
                .filter(AuditLog.timestamp <= date_to) if date_to else AuditLog.status
                .group_by(AuditLog.status)
                .all()
            )

            top_users_query = self.db_session.query(
                AuditLog.user_id,
                AuditLog.username,
                func.count(AuditLog.id).label('count')
            ).filter(
                AuditLog.user_id.isnot(None)
            )
            if date_from:
                top_users_query = top_users_query.filter(AuditLog.timestamp >= date_from)
            if date_to:
                top_users_query = top_users_query.filter(AuditLog.timestamp <= date_to)

            top_users = top_users_query.group_by(
                AuditLog.user_id, AuditLog.username
            ).order_by(
                desc('count')
            ).limit(10).all()

            return {
                'total': total,
                'by_action': by_action,
                'by_entity': by_entity,
                'by_status': by_status,
                'top_users': [
                    {'user_id': u[0], 'username': u[1], 'count': u[2]}
                    for u in top_users
                ],
                'period': {
                    'from': date_from.isoformat() if date_from else None,
                    'to': date_to.isoformat() if date_to else None
                }
            }
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des statistiques d'audit: {e}")
            return {}

    def search_audit_logs(
        self,
        search_term: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            search_filter = or_(
                AuditLog.username.contains(search_term),
                AuditLog.request_path.contains(search_term),
                AuditLog.entity_id.contains(search_term),
                AuditLog.error_message.contains(search_term)
            )

            logs = self.db_session.query(AuditLog).filter(search_filter)\
                         .order_by(desc(AuditLog.timestamp))\
                         .limit(limit).all()

            result = []
            for log in logs:
                log_dict = {
                    'id': log.id,
                    'action': log.action,
                    'entity_type': log.entity_type,
                    'entity_id': log.entity_id,
                    'user_id': log.user_id,
                    'username': log.username,
                    'user_role': log.user_role,
                    'old_data': json.loads(log.old_data) if log.old_data else None,
                    'new_data': json.loads(log.new_data) if log.new_data else None,
                    'changes': json.loads(log.changes) if log.changes else None,
                    'user_ip': log.user_ip,
                    'user_agent': log.user_agent,
                    'request_method': log.request_method,
                    'request_path': log.request_path,
                    'duration_ms': log.duration_ms,
                    'status': log.status,
                    'error_message': log.error_message,
                    'response_status': log.response_status,
                    'is_sensitive': bool(log.is_sensitive),
                    'timestamp': log.timestamp.isoformat() if hasattr(log.timestamp, 'isoformat') else str(log.timestamp),
                    'metadata_ext': json.loads(log.metadata_ext) if log.metadata_ext else None
                }
                result.append(log_dict)
            return result
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la recherche des logs d'audit: {e}")
            return []

    def get_sensitive_actions(
        self,
        date_from: datetime = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            return self.get_audit_logs(
                is_sensitive=True,
                date_from=date_from,
                limit=limit
            )
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des actions sensibles: {e}")
            return []

    def get_action_statistics(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        try:
            query = self.db_session.query(AuditLog)

            if date_from:
                query = query.filter(AuditLog.timestamp >= date_from)
            if date_to:
                query = query.filter(AuditLog.timestamp <= date_to)

            total = query.count()

            action_counts_query = self.db_session.query(
                AuditLog.action,
                func.count(AuditLog.id).label('count')
            )
            if date_from:
                action_counts_query = action_counts_query.filter(AuditLog.timestamp >= date_from)
            if date_to:
                action_counts_query = action_counts_query.filter(AuditLog.timestamp <= date_to)

            action_counts = action_counts_query.group_by(AuditLog.action)\
                                           .order_by(desc('count'))\
                                           .all()

            statistics = []
            for action, count in action_counts:
                percentage = (count / total * 100) if total > 0 else 0
                statistics.append({
                    'action': action,
                    'count': count,
                    'percentage': round(percentage, 2)
                })

            return {
                'total': total,
                'by_action': statistics
            }
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des statistiques d'action: {e}")
            return {}

    def get_top_users(
        self,
        date_from: datetime = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            query = self.db_session.query(
                AuditLog.user_id,
                AuditLog.username,
                AuditLog.user_role,
                func.count(AuditLog.id).label('action_count')
            ).filter(
                AuditLog.user_id.isnot(None)
            )

            if date_from:
                query = query.filter(AuditLog.timestamp >= date_from)

            top_users = query.group_by(
                AuditLog.user_id,
                AuditLog.username,
                AuditLog.user_role
            ).order_by(
                desc('action_count')
            ).limit(limit).all()

            return [
                {
                    'user_id': u[0],
                    'username': u[1],
                    'role': u[2],
                    'action_count': u[3]
                }
                for u in top_users
            ]
        except sql_exceptions.SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des utilisateurs les plus actifs: {e}")
            return []

    def _calculate_diff(self, old_data: dict, new_data: dict) -> dict:
        changes = {}
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
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            deleted = self.db_session.query(AuditLog).filter(
                AuditLog.timestamp < cutoff_date,
                AuditLog.is_sensitive == False
            ).delete()
            self.db_session.flush()
            return deleted
        except sql_exceptions.SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erreur lors du nettoyage des anciens logs: {e}")
            return 0
