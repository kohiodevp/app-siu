"""
Document Controller for file upload/download API endpoints
Story 6.1: Gestion des documents liés aux parcelles
"""

import re
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
from backend.services.document_service import DocumentService
from backend.services.admin_service import AdminService
from backend.models.user import User
from backend.dependencies import get_current_user, require_admin, get_db

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.get("/list")
async def get_documents(
    parcel_id: Optional[str] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get all documents, optionally filtered by parcel_id or document_type
    
    **Requires**: Authentication
    """
    try:
        document_service = DocumentService(db)
        
        if parcel_id:
            documents = document_service.get_documents_by_parcel(parcel_id)
        else:
            # Return all documents if no parcel_id specified
            documents = document_service.get_all_documents()
        
        return {
            "items": [doc.to_dict() for doc in documents],
            "total": len(documents)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching documents: {str(e)}"
        )


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    parcel_id: Optional[str] = Form(None),
    document_type: str = Form(...),
    description: str = Form(""),
    is_public: bool = Form(False),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Upload a document associated with a parcel

    **Story 6.1: Gestion des documents liés aux parcelles**
    **AC1**: Administrateurs peuvent télécharger des documents

    **Requires**: Admin or Manager role
    **Max Size**: 10MB
    **Allowed Types**: PDF, JPG, PNG, DOC, DOCX, XLS, XLSX, TIF
    """
    # Validation des IDs pour prévenir les injections
    # Note: On permet des IDs non-UUID (ex: références manuelles) ou vides
    if parcel_id and len(parcel_id) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parcel ID too long"
        )

    # Validation du type de document
    allowed_types = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'tif', 'tiff', 'txt', 'rtf']
    if document_type.lower() not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document type not allowed. Allowed types: {', '.join(allowed_types)}"
        )

    # Validation de la description pour prévenir les injections
    if description and len(description) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description too long"
        )

    # Validation du fichier
    if not file.filename or len(file.filename) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )

    # Vérification de la taille du fichier (10MB max)
    # Remarque: FastAPI ne permet pas de lire la taille directement sans lire le contenu
    # Nous devons donc limiter cela dans la configuration du serveur ou dans le service

    # Create service with DB session
    document_service = DocumentService(db)

    # Upload document - Pass the file object directly, not the read content
    result = document_service.upload_document(
        file=file.file,  # Use the underlying file object
        parcel_id=parcel_id or "",  # Keep as string to match document model, handle None
        title=file.filename or "Document sans titre",  # Use filename as title
        filename=file.filename or "unknown_file",
        document_type=document_type,
        uploaded_by=current_user.id,  # User ID is string
        description=description
    )

    if not result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Upload failed')
        )

    return result


@router.get("/{document_id}", status_code=status.HTTP_200_OK)
def get_document_metadata(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get document metadata

    **AC3**: Utilisateurs peuvent consulter les métadonnées des documents
    **Requires**: Authentication
    """
    # Validation de l'ID du document pour prévenir les injections
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', document_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID format"
        )

    document_service = DocumentService(db)
    document = document_service.get_document_by_id(document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Check permissions for private documents
    if not document.is_public:
        from backend.models.user import UserRole
        # Allow access to document owner, admins, and managers
        # Deny access if user is not admin/manager AND didn't upload the document
        if (current_user.role not in [UserRole.ADMINISTRATOR, UserRole.MANAGER] and
            document.uploaded_by != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

    return document.to_dict()


@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Download document file

    **AC4**: Utilisateurs peuvent télécharger les documents
    **Requires**: Authentication + permissions
    """
    # Validation de l'ID du document pour prévenir les injections
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', document_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID format"
        )

    document_service = DocumentService(db)

    # Récupérer le document pour vérifier les permissions
    document = document_service.get_document_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Vérifier les permissions d'accès
    from backend.models.user import UserRole
    if not document.is_public:
        # Allow access to document owner, admins, and managers
        # Deny access if user is not admin/manager AND didn't upload the document
        if (current_user.role not in [UserRole.ADMINISTRATOR, UserRole.MANAGER] and
            document.uploaded_by != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé: document privé"
            )

    result = document_service.download_document(document_id, current_user.id)

    if not result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result.get('error', 'Download failed')
        )

    # Validation du chemin du fichier pour éviter les traversées de répertoires
    import os
    from pathlib import Path
    safe_path = os.path.abspath(result['file_path'])
    base_path = os.path.abspath("uploads/")  # Chemin de base pour les téléchargements

    if not safe_path.startswith(base_path):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé: chemin de fichier non autorisé"
        )

    return FileResponse(
        path=result['file_path'],
        filename=result['original_filename'],
        media_type=result['mime_type']
    )


@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
def delete_document(
    document_id: str,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Delete a document

    **Requires**: Admin or Manager role
    """
    # Validation de l'ID du document pour prévenir les injections
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', document_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID format"
        )

    document_service = DocumentService(db)
    result = document_service.delete_document(document_id, current_user.id)

    if not result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Delete failed')
        )

    return result


# Parcel-specific endpoints
@router.get("/parcel/{parcel_id}/list", status_code=status.HTTP_200_OK)
def list_parcel_documents(
    parcel_id: str,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    List all documents for a parcel

    **AC3**: Utilisateurs peuvent consulter les documents liés à une parcelle
    **Requires**: Authentication
    """
    # Validation de l'ID de la parcelle pour prévenir les injections
    if not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', parcel_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parcel ID format"
        )

    # Validation du type de document si fourni
    if document_type:
        allowed_types = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'tif', 'tiff', 'txt', 'rtf']
        if document_type.lower() not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document type not allowed. Allowed types: {', '.join(allowed_types)}"
            )

    document_service = DocumentService(db)

    # Vérifier les permissions - les utilisateurs non-admin ne peuvent voir que les documents publics
    # ou ceux liés à leurs propres parcelles (dans une implémentation complète)
    from backend.models.user import UserRole
    if current_user.role not in [UserRole.ADMINISTRATOR, UserRole.MANAGER]:
        # Pour les utilisateurs non-admin, on pourrait vérifier s'ils ont un lien avec la parcelle
        # Pour l'instant, on limite à l'utilisateur actuel
        pass  # Dans une implémentation complète, on vérifierait l'appartenance à la parcelle

    documents = document_service.get_documents_by_parcel(parcel_id)
    return [doc.to_dict() for doc in documents]


@router.get("/parcel/{parcel_id}", status_code=status.HTTP_200_OK)
def get_documents_by_parcel(
    parcel_id: str,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get all documents for a parcel (compatible avec l'interface Angular)

    **Requires**: Authentication
    """
    document_service = DocumentService(db)
    documents = document_service.get_documents_by_parcel(parcel_id)
    return [doc.to_dict() for doc in documents]


@router.post("/upload-multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_documents(
    files: list[UploadFile] = File(...),
    parcel_id: str = Form(...),
    document_type: str = Form(...),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    """
    Upload multiple documents at once
    
    **Requires**: Admin or Manager role
    """
    document_service = DocumentService(db)
    results = {"success": [], "errors": []}
    
    for file in files:
        result = document_service.upload_document(
            file=file.file,  # Use the underlying file object
            parcel_id=parcel_id,  # Keep as string to match document model
            title=file.filename or "Document sans titre",  # Use filename as title
            filename=file.filename or "unknown_file",
            document_type=document_type,
            uploaded_by=current_user.id,  # User ID is string
            description=""
        )
        
        if result.get('success'):
            results["success"].append({
                "filename": file.filename,
                "document": result.get('document')
            })
        else:
            results["errors"].append({
                "filename": file.filename,
                "error": result.get('error')
            })
    
    return results


@router.get("/search", status_code=status.HTTP_200_OK)
def search_documents(
    query: Optional[str] = None,
    parcel_id: Optional[str] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search documents with multiple criteria

    **Requires**: Authentication
    """
    document_service = DocumentService(db)
    documents = document_service.search_documents(
        search_term=query,
        parcel_id=parcel_id,
        document_type=document_type
    )
    return [doc.to_dict() for doc in documents]


@router.get("/stats", status_code=status.HTTP_200_OK)
def get_document_stats(
    current_user: User = Depends(require_admin)
):
    """
    Get storage statistics

    **Requires**: Admin role
    """
    document_service = DocumentService(db)
    stats = document_service.get_document_stats()
    return stats
