"""
Middleware pour l'audit automatique des requêtes HTTP
Capture toutes les requêtes avec contexte complet
"""

import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour capturer et auditer toutes les requêtes HTTP
    """
    
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        # Chemins à exclure de l'audit (health checks, static files, etc.)
        self.excluded_paths = excluded_paths or [
            '/health',
            '/metrics',
            '/static/',
            '/assets/',
            '/favicon.ico'
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Intercepte toutes les requêtes et enregistre dans l'audit log
        """
        # Vérifier si le chemin doit être exclu
        if self._should_exclude(request.url.path):
            return await call_next(request)
        
        # Capturer le temps de début
        start_time = time.time()
        
        # Extraire le contexte
        user_id = None
        username = None
        user_role = None
        
        # Extraire l'utilisateur du contexte (si authentifié)
        if hasattr(request.state, 'user'):
            user = request.state.user
            user_id = getattr(user, 'id', None)
            username = getattr(user, 'username', None) or getattr(user, 'email', None)
            user_role = getattr(user, 'role', None)
        
        # Extraire les informations réseau
        user_ip = self._get_client_ip(request)
        user_agent = request.headers.get('user-agent', '')
        
        # Déterminer l'action et l'entité depuis le path
        action, entity_type, entity_id = self._parse_request_path(
            request.method,
            request.url.path
        )
        
        # Exécuter la requête
        response = None
        error_message = None
        status = "success"
        
        try:
            response = await call_next(request)
            
            # Vérifier si c'est une erreur
            if response.status_code >= 400:
                status = "failure"
                
        except Exception as e:
            status = "failure"
            error_message = str(e)
            raise
        finally:
            # Calculer la durée
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Enregistrer dans l'audit log (async via background task)
            if response and self._should_audit(request.method, response.status_code):
                # Créer le log en arrière-plan pour ne pas bloquer la réponse
                try:
                    self._log_to_audit(
                        action=action,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        user_id=user_id,
                        username=username,
                        user_role=user_role,
                        user_ip=user_ip,
                        user_agent=user_agent,
                        request_method=request.method,
                        request_path=request.url.path,
                        duration_ms=duration_ms,
                        status=status,
                        error_message=error_message,
                        response_status=response.status_code if response else None,
                        response_size=len(response.body) if response and hasattr(response, 'body') else None
                    )
                except Exception as e:
                    # Ne pas faire échouer la requête si l'audit échoue
                    print(f"Erreur lors de l'audit : {e}")
        
        return response
    
    def _should_exclude(self, path: str) -> bool:
        """Vérifie si le chemin doit être exclu de l'audit"""
        return any(path.startswith(excluded) for excluded in self.excluded_paths)
    
    def _should_audit(self, method: str, status_code: int) -> bool:
        """Détermine si la requête doit être auditée"""
        # Auditer les modifications (POST, PUT, DELETE) et les erreurs
        if method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return True
        
        # Auditer les erreurs même sur GET
        if status_code >= 400:
            return True
        
        # Ne pas auditer les lectures réussies (trop volumineux)
        # Optionnel : activer si besoin de tout tracer
        return False
    
    def _get_client_ip(self, request: Request) -> str:
        """Récupère l'IP du client (gère les proxies)"""
        # Vérifier les headers de proxy
        forwarded = request.headers.get('x-forwarded-for')
        if forwarded:
            return forwarded.split(',')[0].strip()
        
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip
        
        # IP directe
        if request.client:
            return request.client.host
        
        return 'unknown'
    
    def _parse_request_path(self, method: str, path: str) -> tuple:
        """
        Parse le path pour extraire action, entity_type, entity_id
        
        Returns:
            tuple: (action, entity_type, entity_id)
        """
        # Mapper les méthodes HTTP aux actions
        action_map = {
            'POST': 'create',
            'GET': 'read',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        
        action = action_map.get(method, 'unknown')
        
        # Parser le path
        # Ex: /api/parcels/123 -> entity_type=parcel, entity_id=123
        parts = [p for p in path.split('/') if p]
        
        entity_type = None
        entity_id = None
        
        if len(parts) >= 2:
            # Chercher le type d'entité (après /api)
            if 'api' in parts:
                api_index = parts.index('api')
                if len(parts) > api_index + 1:
                    entity_type = parts[api_index + 1].rstrip('s')  # parcels -> parcel
                    
                    # Chercher l'ID (numérique après le type)
                    if len(parts) > api_index + 2:
                        potential_id = parts[api_index + 2]
                        if potential_id.isdigit() or len(potential_id) == 36:  # ID ou UUID
                            entity_id = potential_id
        
        # Actions spéciales
        if 'login' in path:
            action = 'login'
            entity_type = 'user'
        elif 'logout' in path:
            action = 'logout'
            entity_type = 'user'
        elif 'upload' in path:
            action = 'upload'
        elif 'download' in path:
            action = 'download'
        
        return action, entity_type, entity_id
    
    def _log_to_audit(self, **kwargs):
        """
        Enregistre dans l'audit log
        Note: Doit être appelé de manière asynchrone ou en background
        """
        try:
            from backend.database import SessionLocal
            from backend.services.audit_service import AuditService

            # Créer une session SQLAlchemy
            db = SessionLocal()

            try:
                audit_service = AuditService(db)
                audit_service.log_action(**kwargs)
            finally:
                db.close()

        except Exception as e:
            print(f"Erreur _log_to_audit : {e}")


def setup_audit_middleware(app, excluded_paths: list = None):
    """
    Configure le middleware d'audit sur l'application
    
    Args:
        app: Instance FastAPI
        excluded_paths: Liste des chemins à exclure
    """
    app.add_middleware(AuditMiddleware, excluded_paths=excluded_paths)
    print("✅ Audit middleware configuré")
