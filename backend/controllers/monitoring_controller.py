"""
Monitoring Controller - Métriques système et health checks
"""

import re
from fastapi import APIRouter, Depends, status
from datetime import datetime, timedelta
import psutil
import os
from typing import Dict, Any

from backend.dependencies import require_admin
from backend.models.user import User

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint pour load balancers et monitoring
    
    **Public endpoint** - Pas d'authentification requise
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_system_metrics(current_user: User = Depends(require_admin)):
    """
    Métriques système en temps réel
    
    **Requires**: Admin role
    
    **Returns**:
    - CPU usage
    - Memory usage
    - Disk usage
    - Network stats
    - Process info
    """
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    # Memory
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disk
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    
    # Network
    net_io = psutil.net_io_counters()
    
    # Process
    process = psutil.Process(os.getpid())
    process_memory = process.memory_info()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu": {
            "usage_percent": cpu_percent,
            "count": cpu_count,
            "frequency_mhz": cpu_freq.current if cpu_freq else None
        },
        "memory": {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent,
            "swap_total_gb": round(swap.total / (1024**3), 2),
            "swap_used_gb": round(swap.used / (1024**3), 2),
            "swap_percent": swap.percent
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
            "read_mb": round(disk_io.read_bytes / (1024**2), 2) if disk_io else None,
            "write_mb": round(disk_io.write_bytes / (1024**2), 2) if disk_io else None
        },
        "network": {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errors_in": net_io.errin,
            "errors_out": net_io.errout
        },
        "process": {
            "pid": os.getpid(),
            "memory_mb": round(process_memory.rss / (1024**2), 2),
            "cpu_percent": process.cpu_percent(),
            "threads": process.num_threads(),
            "connections": len(process.connections())
        }
    }


@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_application_stats(current_user: User = Depends(require_admin)):
    """
    Statistiques application
    
    **Requires**: Admin role
    
    **Returns**:
    - Nombre total d'entités
    - Activité récente
    - Performance metrics
    """
    from backend.database import SessionLocal
    from backend.models.parcel import Parcel
    from backend.models.document import Document
    from backend.models.user import User as UserModel
    from backend.models.audit_log import AuditLog
    
    db = SessionLocal()
    
    try:
        # Compter les entités
        total_parcels = db.query(Parcel).count()
        total_documents = db.query(Document).filter(Document.deleted == False).count()
        total_users = db.query(UserModel).count()
        total_audit_logs = db.query(AuditLog).count()
        
        # Activité dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_parcels = db.query(Parcel).filter(Parcel.created_at >= yesterday).count()
        recent_documents = db.query(Document).filter(Document.uploaded_at >= yesterday).count()
        recent_audit_logs = db.query(AuditLog).filter(AuditLog.timestamp >= yesterday).count()
        
        # WebSocket connections
        from backend.services.websocket_service import manager
        active_connections = manager.get_active_users_count()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "entities": {
                "parcels": total_parcels,
                "documents": total_documents,
                "users": total_users,
                "audit_logs": total_audit_logs
            },
            "recent_24h": {
                "parcels_created": recent_parcels,
                "documents_uploaded": recent_documents,
                "audit_logs": recent_audit_logs
            },
            "realtime": {
                "websocket_connections": active_connections
            },
            "uptime": get_uptime()
        }
    finally:
        db.close()


@router.get("/database", status_code=status.HTTP_200_OK)
async def get_database_stats(current_user: User = Depends(require_admin)):
    """
    Statistiques base de données

    **Requires**: Admin role
    """
    from backend.config import settings
    import sqlite3
    import os

    # Validation du chemin de la base de données pour éviter les traversées de répertoires
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')

    # Normaliser le chemin pour éviter les traversées de répertoires
    normalized_path = os.path.normpath(db_path)
    base_path = os.path.normpath(os.path.dirname(settings.DATABASE_URL.replace('sqlite:///', '')))

    # Vérifier que le chemin est dans le répertoire attendu
    if not normalized_path.startswith(base_path):
        return {
            "error": "Invalid database path"
        }

    if os.path.exists(normalized_path):
        db_size_mb = round(os.path.getsize(normalized_path) / (1024**2), 2)

        # SQLite stats
        conn = sqlite3.connect(normalized_path)
        cursor = conn.cursor()

        # Obtenir les noms des tables de manière sécurisée
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()

        table_stats = []
        for table in tables:
            # Validation du nom de table pour éviter les injections SQL
            if not re.match(r'^[a-zA-Z0-9_]+$', table[0]):
                continue  # Ignorer les noms de table non valides

            # Utiliser une requête paramétrée pour compter les lignes
            # NOTE: Le nom de table est validé ci-dessus avec une expression régulière stricte
            # pour éviter les injections SQL
            query = f"SELECT COUNT(*) FROM [{table[0]}]"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            table_stats.append({
                "name": table[0],
                "rows": count
            })

        conn.close()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "database": {
                "path": normalized_path,
                "size_mb": db_size_mb,
                "tables": table_stats
            }
        }
    else:
        return {
            "error": "Database file not found"
        }


def get_uptime() -> str:
    """Calcule l'uptime du système"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    return f"{days}d {hours}h {minutes}m"


@router.get("/alerts", status_code=status.HTTP_200_OK)
async def get_system_alerts(current_user: User = Depends(require_admin)):
    """
    Génère des alertes basées sur les métriques système
    
    **Requires**: Admin role
    """
    alerts = []
    
    # CPU alert
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        alerts.append({
            "severity": "warning" if cpu_percent < 90 else "critical",
            "metric": "cpu",
            "value": cpu_percent,
            "threshold": 80,
            "message": f"CPU usage is high: {cpu_percent}%"
        })
    
    # Memory alert
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        alerts.append({
            "severity": "warning" if memory.percent < 90 else "critical",
            "metric": "memory",
            "value": memory.percent,
            "threshold": 80,
            "message": f"Memory usage is high: {memory.percent}%"
        })
    
    # Disk alert
    disk = psutil.disk_usage('/')
    if disk.percent > 80:
        alerts.append({
            "severity": "warning" if disk.percent < 90 else "critical",
            "metric": "disk",
            "value": disk.percent,
            "threshold": 80,
            "message": f"Disk usage is high: {disk.percent}%"
        })
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "alerts": alerts,
        "count": len(alerts),
        "status": "healthy" if len(alerts) == 0 else "degraded" if all(a['severity'] == 'warning' for a in alerts) else "critical"
    }
