"""
Service de validation et sécurité des documents
"""
import mimetypes
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import io

# Try to import python-magic, but make it optional for Windows
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError) as e:
    MAGIC_AVAILABLE = False
    print(f"Warning: python-magic not available ({e}). Using mimetypes fallback for MIME detection.")

class DocumentValidator:
    """Validateur de documents avec vérifications de sécurité"""
    
    # Extensions autorisées par type de document
    ALLOWED_EXTENSIONS = {
        'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'},
        'document': {'pdf', 'doc', 'docx', 'odt', 'txt'},
        'spreadsheet': {'xls', 'xlsx', 'ods', 'csv'},
        'archive': {'zip', 'rar', '7z'},
        'cad': {'dwg', 'dxf'},
    }
    
    # MIME types autorisés
    ALLOWED_MIME_TYPES = {
        'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/tiff', 'image/webp',
        'application/pdf',
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
    
    def __init__(self, max_file_size_mb: int = 50):
        self.max_file_size = max_file_size_mb * 1024 * 1024  # Convertir en octets
    
    def validate_file(self, file_data: bytes, filename: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Valide un fichier uploadé
        
        Args:
            file_data: Données du fichier
            filename: Nom du fichier
            
        Returns:
            tuple: (is_valid, error_message, mime_type)
        """
        # 1. Vérifier la taille
        file_size = len(file_data)
        if file_size > self.max_file_size:
            return False, f"Fichier trop volumineux. Maximum {self.max_file_size // (1024*1024)} MB", None
        
        if file_size == 0:
            return False, "Fichier vide", None
        
        # 2. Vérifier l'extension
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if not self._is_extension_allowed(extension):
            return False, f"Extension '{extension}' non autorisée", None
        
        # 3. Détecter le MIME type réel (magic numbers)
        try:
            mime_type = magic.from_buffer(file_data, mime=True)
        except Exception:
            # Fallback sur mimetypes si python-magic n'est pas disponible
            mime_type, _ = mimetypes.guess_type(filename)
        
        if not mime_type:
            return False, "Impossible de déterminer le type de fichier", None
        
        # 4. Vérifier que le MIME type est autorisé
        if mime_type not in self.ALLOWED_MIME_TYPES:
            return False, f"Type de fichier '{mime_type}' non autorisé", None
        
        # 5. Vérification supplémentaire pour les images
        if mime_type.startswith('image/'):
            is_valid_image, error = self._validate_image(file_data)
            if not is_valid_image:
                return False, error, None
        
        # 6. Vérifier que l'extension correspond au MIME type
        expected_extensions = mimetypes.guess_all_extensions(mime_type)
        if expected_extensions and f'.{extension}' not in expected_extensions:
            return False, f"Extension '{extension}' ne correspond pas au type de fichier '{mime_type}'", None
        
        return True, None, mime_type
    
    def _is_extension_allowed(self, extension: str) -> bool:
        """Vérifie si une extension est autorisée"""
        all_extensions = set()
        for exts in self.ALLOWED_EXTENSIONS.values():
            all_extensions.update(exts)
        return extension.lower() in all_extensions
    
    def _validate_image(self, file_data: bytes) -> Tuple[bool, Optional[str]]:
        """
        Valide qu'une image est correcte et non corrompue
        
        Args:
            file_data: Données de l'image
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            img = Image.open(io.BytesIO(file_data))
            img.verify()  # Vérifie que l'image n'est pas corrompue
            
            # Vérifier les dimensions (éviter les bombes de décompression)
            if img.width * img.height > 100_000_000:  # 100 MP maximum
                return False, "Image trop grande (résolution maximale : 100 MP)"
            
            return True, None
        except Exception as e:
            return False, f"Image invalide ou corrompue : {str(e)}"
    
    def generate_thumbnail(self, file_data: bytes, size: Tuple[int, int] = (200, 200)) -> Optional[bytes]:
        """
        Génère une miniature pour une image
        
        Args:
            file_data: Données de l'image
            size: Taille de la miniature (largeur, hauteur)
            
        Returns:
            bytes: Données de la miniature ou None en cas d'erreur
        """
        try:
            img = Image.open(io.BytesIO(file_data))
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Convertir en RGB si nécessaire (pour sauvegarder en JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            
            # Sauvegarder dans un buffer
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
        except Exception as e:
            print(f"Erreur lors de la génération de la miniature : {e}")
            return None
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Nettoie un nom de fichier pour éviter les injections

        Args:
            filename: Nom du fichier original

        Returns:
            str: Nom de fichier sécurisé
        """
        # Validation du nom de fichier pour éviter les traversées de chemin
        import re
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError("Invalid filename: contains path traversal characters")

        # Retirer les caractères dangereux
        dangerous_chars = ['/', '\\', '..', '\x00', '\n', '\r', '\t']
        safe_name = filename
        for char in dangerous_chars:
            safe_name = safe_name.replace(char, '_')

        # Limiter la longueur
        if len(safe_name) > 255:
            name, ext = safe_name.rsplit('.', 1) if '.' in safe_name else (safe_name, '')
            safe_name = name[:250] + ('.' + ext if ext else '')

        return safe_name
    
    def check_file_integrity(self, file_path: Path, expected_checksum: str) -> bool:
        """
        Vérifie l'intégrité d'un fichier avec son checksum
        
        Args:
            file_path: Chemin du fichier
            expected_checksum: Checksum attendu (SHA-256)
            
        Returns:
            bool: True si l'intégrité est vérifiée
        """
        import hashlib
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest() == expected_checksum
        except Exception:
            return False
