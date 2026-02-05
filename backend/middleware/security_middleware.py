"""
Middleware de sécurité avancé
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from backend.core.security import rate_limiter, security_validator

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware de sécurité pour toutes les requêtes"""
    
    async def dispatch(self, request: Request, call_next):
        # Vérifier les headers de sécurité
        client_ip = request.client.host
        
        # Rate limiting global (100 req/min par IP)
        if rate_limiter.is_rate_limited(f"ip_{client_ip}", max_requests=100, window_seconds=60):
            raise HTTPException(status_code=429, detail="Too many requests")
        
        # Ajouter les headers de sécurité à la réponse
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
