import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_database_url():
    """
    Retourne l'URL de la base de données.
    Utilise une variable d'environnement si disponible, sinon une valeur par défaut.
    """
    db_url_from_env = os.getenv('DATABASE_URL')
    if db_url_from_env:
        return db_url_from_env
    else:
        # Le chemin est relatif à la racine du projet où la commande est lancée
        return "sqlite:///./siu_database.db"

SQLALCHEMY_DATABASE_URL = get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args est spécifique à SQLite. Il n'est pas nécessaire pour d'autres BDD.
    connect_args={"check_same_thread": False}
)

# Crée une classe SessionLocal. Chaque instance de SessionLocal sera une session de base de données.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles SQLAlchemy.
# Nos modèles ORM hériteront de cette classe.
Base = declarative_base()

def get_db():
    """
    Dépendance FastAPI pour obtenir une session de base de données.
    - Ouvre une session au début de la requête.
    - Fournit la session à la fonction de la route.
    - Ferme la session à la fin de la requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Crée toutes les tables dans la base de données.
    Ceci est appelé au démarrage de l'application.
    Les modèles doivent être importés quelque part pour que Base les connaisse.
    """
    # Importer tous les modèles ici pour qu'ils soient enregistrés avec Base
    from backend.models import user, parcel, document, alert, audit_log, mutation, zone, permit
    print("Initialisation de la base de données et création des tables si elles n'existent pas...")
    Base.metadata.create_all(bind=engine)
    print("Tables initialisées.")

if __name__ == '__main__':
    print(f"Utilisation de la base de données à l'URL : {SQLALCHEMY_DATABASE_URL}")
    init_db()