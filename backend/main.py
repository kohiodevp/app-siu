import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.controllers import user_controller, auth_controller, parcel_controller, document_controller, dashboard_controller, audit_controller, report_controller, websocket_controller, monitoring_controller, mutation_controller, analytics_controller, permit_controller, zone_controller, advanced_features_controller, search_controller
from backend.controllers.activity_controller import activity_controller
from backend.controllers.analytics_charts_controller import router as analytics_charts_router
from backend.config import CORS_ORIGINS
from backend.middleware.rate_limit_middleware import setup_rate_limiting
from backend.container_config import configure_container

# Créer l'instance de l'application FastAPI
app = FastAPI(
    title="SIU - Système d'Information Urbain",
    description="API pour la gestion des parcelles et des droits fonciers.",
    version="1.0.0"
)

# Configurer le conteneur d'injection de dépendances
configure_container()


# Configuration CORS - DOIT être ajouté AVANT les routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Origines autorisées (Angular, etc.)
    allow_credentials=True,       # Autoriser les cookies/sessions
    allow_methods=["*"],          # Autoriser toutes les méthodes HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # Autoriser tous les headers
)

# Setup rate limiting for authentication endpoints
setup_rate_limiting(app)

# Inclure les routeurs des contrôleurs
app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(parcel_controller.router)
app.include_router(document_controller.router)
app.include_router(dashboard_controller.router)
app.include_router(audit_controller.router)
app.include_router(websocket_controller.router)
app.include_router(mutation_controller.router)
app.include_router(monitoring_controller.router)
app.include_router(report_controller.router)
app.include_router(activity_controller.router)
app.include_router(analytics_controller.router)
app.include_router(analytics_charts_router)
app.include_router(permit_controller.router)
app.include_router(zone_controller.router)
app.include_router(advanced_features_controller.router)
app.include_router(search_controller.router)

# Health check endpoint (must be before catch-all routes)

# Configuration pour servir l'application Angular en production
ANGULAR_DIST_PATH = Path(__file__).parent.parent / "dist" / "siu-angular" / "browser"

if ANGULAR_DIST_PATH.exists():
    # Servir les fichiers statiques Angular
    assets_path = ANGULAR_DIST_PATH / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    
    # Catch-all route pour Angular (doit être en dernier)
    @app.get("/{full_path:path}")
    async def serve_angular(full_path: str):
        """
        Sert l'application Angular pour toutes les routes non-API.
        Permet le routing côté client d'Angular.
        """
        # NE PAS intercepter les routes API
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API route not found")
        
        # Si c'est un fichier statique Angular
        file_path = ANGULAR_DIST_PATH / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Sinon, renvoyer index.html pour le routing Angular
        return FileResponse(ANGULAR_DIST_PATH / "index.html")
else:
    # En développement (Angular sur port 4200)
    @app.get("/", tags=["Root"])
    def read_root():
        """Endpoint racine pour vérifier que l'API est en cours d'exécution."""
        return {
            "message": "Bienvenue sur l'API du SIU",
            "note": "Frontend Angular disponible sur http://localhost:4200"
        }
