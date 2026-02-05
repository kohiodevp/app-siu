"""
Service de gestion du stockage des fichiers
"""
import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, BinaryIO
from werkzeug.utils import secure_filename

class StorageService:
    """Service de stockage sécurisé des fichiers"""
    
    def __init__(self, base_upload_folder: str):
        self.base_upload_folder = Path(base_upload_folder)
        self.base_upload_folder.mkdir(parents=True, exist_ok=True)
    
    def save_document(
        self,
        file: BinaryIO,
        parcel_id: str,  # Changed from int to str to match the actual usage
        document_id: str,  # Changed from int to str to match the actual usage
        filename: str
    ) -> tuple[str, str, int]:
        """
        Sauvegarde un document de manière sécurisée

        Args:
            file: Fichier à sauvegarder
            parcel_id: ID de la parcelle
            document_id: ID du document
            filename: Nom du fichier original

        Returns:
            tuple: (file_path, checksum, file_size)
        """
        # Valider les IDs pour éviter la traversée de chemin
        import re
        safe_parcel_id = str(parcel_id)
        if not safe_parcel_id:
            safe_parcel_id = "unassigned"
        elif not re.match(r'^[a-zA-Z0-9_-]+$', safe_parcel_id):
            raise ValueError("Invalid parcel_id: must contain only alphanumeric characters, hyphens, and underscores")

        if not re.match(r'^[a-zA-Z0-9_-]+$', str(document_id)):
            raise ValueError("Invalid document_id: must contain only alphanumeric characters, hyphens, and underscores")

        # Validation du nom de fichier pour éviter les injections
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError("Invalid filename: contains path traversal characters")

        # Sécuriser le nom de fichier
        safe_filename = secure_filename(filename)

        # Créer le chemin de stockage organisé
        # Utiliser des chemins sécurisés sans possibilité de traversée
        parcel_folder = self.base_upload_folder / "parcels" / safe_parcel_id / "documents"
        parcel_folder.mkdir(parents=True, exist_ok=True)

        # Vérifier que le chemin résultant est bien dans le répertoire de base
        resolved_path = (parcel_folder / "dummy").resolve()
        base_path = self.base_upload_folder.resolve()
        if not str(resolved_path).startswith(str(base_path)):
            raise ValueError("Invalid path construction - potential path traversal detected")

        # Ajouter extension basée sur l'ID du document pour unicité
        file_extension = safe_filename.rsplit('.', 1)[1] if '.' in safe_filename else ''
        stored_filename = f"{document_id}.{file_extension}" if file_extension else str(document_id)
        file_path = parcel_folder / stored_filename

        # Calculer checksum pendant l'écriture
        checksum = hashlib.sha256()
        file_size = 0

        with open(file_path, 'wb') as f:
            while chunk := file.read(8192):  # Lire par blocs de 8KB
                checksum.update(chunk)
                f.write(chunk)
                file_size += len(chunk)

        # Retourner le chemin relatif à base_upload_folder
        relative_path = str(file_path.relative_to(self.base_upload_folder))

        return relative_path, checksum.hexdigest(), file_size
    
    def save_thumbnail(
        self, 
        thumbnail_data: bytes, 
        parcel_id: int, 
        document_id: int
    ) -> str:
        """
        Sauvegarde une miniature
        
        Args:
            thumbnail_data: Données de la miniature
            parcel_id: ID de la parcelle
            document_id: ID du document
            
        Returns:
            str: Chemin relatif de la miniature
        """
        parcel_folder = self.base_upload_folder / "parcels" / str(parcel_id) / "thumbnails"
        parcel_folder.mkdir(parents=True, exist_ok=True)
        
        thumbnail_path = parcel_folder / f"{document_id}_thumb.jpg"
        
        with open(thumbnail_path, 'wb') as f:
            f.write(thumbnail_data)
        
        return str(thumbnail_path.relative_to(self.base_upload_folder))
    
    def get_document_path(self, relative_path: str) -> Path:
        """Retourne le chemin absolu d'un document"""
        return self.base_upload_folder / relative_path
    
    def delete_document(self, relative_path: str) -> bool:
        """
        Supprime un document du stockage
        
        Args:
            relative_path: Chemin relatif du document
            
        Returns:
            bool: True si supprimé avec succès
        """
        try:
            file_path = self.get_document_path(relative_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression du document : {e}")
            return False
    
    def delete_thumbnail(self, relative_path: str) -> bool:
        """Supprime une miniature"""
        return self.delete_document(relative_path)
    
    def get_storage_stats(self) -> dict:
        """
        Retourne des statistiques sur le stockage
        
        Returns:
            dict: Statistiques (nombre de fichiers, taille totale, etc.)
        """
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.base_upload_folder):
            total_files += len(files)
            for file in files:
                file_path = Path(root) / file
                if file_path.exists():
                    total_size += file_path.stat().st_size
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'base_folder': str(self.base_upload_folder)
        }
    
    def cleanup_orphan_files(self, valid_paths: list[str]) -> int:
        """
        Nettoie les fichiers orphelins (pas dans la DB)
        
        Args:
            valid_paths: Liste des chemins de fichiers valides (dans la DB)
            
        Returns:
            int: Nombre de fichiers supprimés
        """
        valid_paths_set = set(valid_paths)
        deleted_count = 0
        
        for root, dirs, files in os.walk(self.base_upload_folder):
            for file in files:
                file_path = Path(root) / file
                relative_path = str(file_path.relative_to(self.base_upload_folder))
                
                if relative_path not in valid_paths_set:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Erreur lors de la suppression de {relative_path}: {e}")
        
        return deleted_count
    
    def backup_document(self, relative_path: str, backup_folder: str) -> Optional[str]:
        """
        Crée une copie de sauvegarde d'un document
        
        Args:
            relative_path: Chemin relatif du document
            backup_folder: Dossier de sauvegarde
            
        Returns:
            str: Chemin du fichier de sauvegarde ou None en cas d'erreur
        """
        try:
            source = self.get_document_path(relative_path)
            if not source.exists():
                return None
            
            backup_path = Path(backup_folder)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Ajouter timestamp au nom du backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{source.stem}_{timestamp}{source.suffix}"
            destination = backup_path / backup_filename
            
            shutil.copy2(source, destination)
            return str(destination)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return None
