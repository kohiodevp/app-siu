"""
Rate limiting middleware for authentication endpoints
"""
import time
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException
from typing import Callable


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware
    Tracks requests by IP address with configurable limits
    """
    
    def __init__(self, app, 
                 max_attempts: int = 5, 
                 window_seconds: int = 300,  # 5 minutes
                 auth_endpoints: list = None):
        super().__init__(app)
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.auth_endpoints = auth_endpoints or ["/api/auth/login"]
        
        # Dictionary to store attempts: {ip: deque of timestamps}
        self.attempts = defaultdict(lambda: deque(maxlen=max_attempts))

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check if this is an authentication endpoint that needs rate limiting
        if request.url.path in self.auth_endpoints:
            client_ip = self._get_client_ip(request)
            
            # Clean old attempts outside the window
            current_time = time.time()
            while (self.attempts[client_ip] and 
                   current_time - self.attempts[client_ip][0] > self.window_seconds):
                self.attempts[client_ip].popleft()
            
            # Check if limit exceeded
            if len(self.attempts[client_ip]) >= self.max_attempts:
                # Too many attempts
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Too many login attempts",
                        "message": f"Maximum {self.max_attempts} attempts per {self.window_seconds} seconds exceeded"
                    }
                )
            
            # Process the request
            response = await call_next(request)
            
            # Record attempt if it was a failed login
            if (response.status_code == 401 or 
                (response.status_code == 200 and 
                 hasattr(response, 'body') and 
                 b'"authenticated":false' in getattr(response, 'body', b''))):
                
                # Only count failed attempts
                self.attempts[client_ip].append(current_time)
            
            return response
        
        # For non-auth endpoints, just pass through
        return await call_next(request)

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        forwarded = request.headers.get('x-forwarded-for')
        if forwarded:
            # Prendre uniquement le premier IP pour éviter les falsifications
            ip_list = [ip.strip() for ip in forwarded.split(',')]
            # Valider que le premier élément est une adresse IP valide
            import re
            first_ip = ip_list[0]
            if re.match(r'^[\d\.]+$', first_ip) or re.match(r'^[0-9a-fA-F:]+$', first_ip):
                return first_ip

        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            # Valider que l'IP est une adresse IP valide
            import re
            if re.match(r'^[\d\.]+$', real_ip) or re.match(r'^[0-9a-fA-F:]+$', real_ip):
                return real_ip

        if request.client:
            return request.client.host

        return 'unknown'


def setup_rate_limiting(app):
    """
    Setup rate limiting middleware for authentication endpoints
    """
    app.add_middleware(
        RateLimitMiddleware,
        max_attempts=5,  # 5 attempts per 5 minutes
        window_seconds=300,
        auth_endpoints=["/api/auth/login"]
    )