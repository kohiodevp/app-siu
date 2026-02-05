"""
WebSocket Controller - Endpoints pour connexions temps réel
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from typing import Optional
import json

from backend.services.websocket_service import manager
from backend.dependencies import get_current_user_ws
from backend.models.user import User

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    token: Optional[str] = None
):
    """
    WebSocket endpoint pour les notifications en temps réel
    
    **URL:** ws://localhost:8000/ws/notifications?token=<JWT_TOKEN>
    
    **Messages reçus:**
    - connection: Confirmation de connexion
    - parcel_created: Nouvelle parcelle créée
    - parcel_updated: Parcelle modifiée
    - document_uploaded: Document uploadé
    - system_alert: Alerte système
    
    **Format des messages:**
    ```json
    {
        "type": "parcel_created",
        "data": {
            "parcel_id": "123",
            "reference": "REF-001",
            "created_by": 1
        },
        "timestamp": "2026-01-25T10:30:00Z"
    }
    ```
    """
    # Authentifier l'utilisateur
    try:
        user = await get_current_user_ws(token)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connecter l'utilisateur
    await manager.connect(websocket, user.id)
    
    try:
        while True:
            # Recevoir les messages du client (heartbeat, subscriptions, etc.)
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                # Gérer les différents types de messages
                if message_type == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
                elif message_type == "join_room":
                    room = message.get("room")
                    if room:
                        await manager.join_room(websocket, room)
                        await manager.send_personal_message({
                            "type": "room_joined",
                            "room": room
                        }, websocket)
                
                elif message_type == "leave_room":
                    room = message.get("room")
                    if room:
                        await manager.leave_room(websocket, room)
                        await manager.send_personal_message({
                            "type": "room_left",
                            "room": room
                        }, websocket)
                
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
    except Exception as e:
        print(f"WebSocket error for user {user.id}: {e}")
        manager.disconnect(websocket, user.id)


@router.get("/status")
async def websocket_status(current_user: User = Depends(get_current_user_ws)):
    """
    Obtenir le statut des connexions WebSocket

    **Requires:** Admin role
    """
    # Vérifier que l'utilisateur est authentifié
    if not current_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Non authentifié")

    # Vérifier que l'utilisateur a le rôle admin
    from backend.models.user import UserRole
    if current_user.role != UserRole.ADMINISTRATOR:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Permissions insuffisantes")

    return {
        "active_users": manager.get_active_users_count(),
        "rooms": list(manager.rooms.keys()),
        "is_online": manager.is_user_online(current_user.id)
    }
