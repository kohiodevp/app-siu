"""
Configuration settings for SIU application
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# CORS settings
CORS_ORIGINS = [
    "http://localhost:4200",  # Angular dev server
    "http://localhost:8000",  # Alternative dev port
    "http://127.0.0.1:4200",  # Alternative localhost
    "http://127.0.0.1:8000",  # Alternative localhost
]

# Charger les origines CORS depuis les variables d'environnement
CORS_ORIGINS_RAW = os.getenv('CORS_ORIGINS', '')
if CORS_ORIGINS_RAW:
    env_origins = [origin.strip() for origin in CORS_ORIGINS_RAW.split(',') if origin.strip()]
    CORS_ORIGINS.extend(env_origins)

# Charger une URL frontend spécifique si définie
FRONTEND_URL = os.getenv('FRONTEND_URL')
if FRONTEND_URL and FRONTEND_URL not in CORS_ORIGINS:
    CORS_ORIGINS.append(FRONTEND_URL)

# En production, ajouter les domaines autorisés via variable d'environnement
PRODUCTION_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
if PRODUCTION_ORIGINS and PRODUCTION_ORIGINS[0]:
    # Valider les origines pour éviter les injections
    import re
    validated_origins = []
    for origin in PRODUCTION_ORIGINS:
        origin = origin.strip()
        # Vérifier que l'origine est une URL valide
        if re.match(r'^https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9])*(:\d+)?$', origin):
            validated_origins.append(origin)

    CORS_ORIGINS.extend(validated_origins)

# Charger les origines CORS depuis la variable d'environnement CORS_ORIGINS (alternative)
CORS_ORIGINS_RAW = os.getenv('CORS_ORIGINS', '')
if CORS_ORIGINS_RAW:
    env_origins = [origin.strip() for origin in CORS_ORIGINS_RAW.split(',') if origin.strip()]
    CORS_ORIGINS.extend(env_origins)

# File upload settings
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # 50 MB
THUMBNAIL_SIZE = (200, 200)
DOCUMENT_RETENTION_DAYS = 365

# Allowed file extensions (étendu)
ALLOWED_EXTENSIONS = {
    'pdf',           # PDF documents
    'jpg', 'jpeg',   # JPEG images
    'png',           # PNG images
    'gif', 'bmp', 'webp',  # Other images
    'doc', 'docx',   # Microsoft Word
    'odt',           # OpenDocument Text
    'txt',           # Plain text
    'xls', 'xlsx',   # Microsoft Excel
    'ods', 'csv',    # Spreadsheets
    'tif', 'tiff',   # TIFF images (for survey plans)
    'zip', 'rar', '7z',  # Archives
    'dwg', 'dxf',    # CAD files
}

# Allowed MIME types (for validation) - Étendu
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 
    'image/tiff', 'image/tif', 'image/webp',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.oasis.opendocument.text',
    'text/plain',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.oasis.opendocument.spreadsheet',
    'text/csv',
    'application/zip',
    'application/x-rar-compressed',
    'application/x-7z-compressed',
}

# Database settings
DATABASE_FILE = os.getenv('SIU_DATABASE_FILE', 'siu_database.db')

# Ensure upload folder exists
def ensure_upload_folder():
    """Create upload folder if it doesn't exist"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Create .gitkeep to preserve folder structure
    gitkeep = os.path.join(UPLOAD_FOLDER, '.gitkeep')
    if not os.path.exists(gitkeep):
        with open(gitkeep, 'w') as f:
            f.write('')

def allowed_file(filename: str) -> bool:
    """
    Check if a filename has an allowed extension
    
    Args:
        filename: Name of the file
        
    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension (lowercase, without dot)
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

# Performance settings
ENABLE_QUERY_MONITORING = True
CACHE_TIMEOUT = 300  # 5 minutes

# Connection pool settings
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# Request limits
MAX_PAGE_SIZE = 1000
DEFAULT_PAGE_SIZE = 100
