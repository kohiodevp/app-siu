"""
WebSocket Service pour notifications en temps réel
Gère les connexions WebSocket et broadcast des événements
"""

from typing import Dict, Set, Any
from datetime import datetime
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Gestionnaire de connexions WebSocket"""
    
    def __init__(self):
        # Connexions actives par user_id
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Connexions par room (pour groupes)
        self.rooms: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accepter une nouvelle connexion"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        
        # Envoyer message de bienvenue
        await self.send_personal_message({
            "type": "connection",
            "message": "Connected to SIU WebSocket",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Déconnecter un client"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            # Supprimer l'entrée si plus de connexions
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        # Retirer des rooms
        for room in self.rooms.values():
            room.discard(websocket)
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Envoyer un message à une connexion spécifique"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def send_to_user(self, message: Dict[str, Any], user_id: int):
        """Envoyer un message à toutes les connexions d'un utilisateur"""
        if user_id in self.active_connections:
            disconnected = set()
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    disconnected.add(connection)
                except Exception as e:
                    print(f"Error sending to user {user_id}: {e}")
                    disconnected.add(connection)
            
            # Nettoyer les connexions mortes
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def broadcast(self, message: Dict[str, Any], exclude_user: int = None):
        """Envoyer un message à tous les utilisateurs connectés"""
        disconnected_users = []
        
        for user_id, connections in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            
            disconnected = set()
            for connection in connections:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    disconnected.add(connection)
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {e}")
                    disconnected.add(connection)
            
            # Nettoyer les connexions mortes
            for conn in disconnected:
                self.disconnect(conn, user_id)
            
            if not self.active_connections[user_id]:
                disconnected_users.append(user_id)
        
        # Nettoyer les utilisateurs sans connexions
        for user_id in disconnected_users:
            if user_id in self.active_connections:
                del self.active_connections[user_id]
    
    async def join_room(self, websocket: WebSocket, room: str):
        """Rejoindre une room (ex: 'parcels', 'documents')"""
        if room not in self.rooms:
            self.rooms[room] = set()
        
        self.rooms[room].add(websocket)
    
    async def leave_room(self, websocket: WebSocket, room: str):
        """Quitter une room"""
        if room in self.rooms:
            self.rooms[room].discard(websocket)
    
    async def broadcast_to_room(self, message: Dict[str, Any], room: str):
        """Envoyer un message à tous les membres d'une room"""
        if room not in self.rooms:
            return
        
        disconnected = set()
        for connection in self.rooms[room]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to room {room}: {e}")
                disconnected.add(connection)
        
        # Nettoyer les connexions mortes
        for conn in disconnected:
            self.rooms[room].discard(conn)
    
    def get_active_users_count(self) -> int:
        """Obtenir le nombre d'utilisateurs connectés"""
        return len(self.active_connections)
    
    def is_user_online(self, user_id: int) -> bool:
        """Vérifier si un utilisateur est connecté"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0


# Instance globale du gestionnaire
manager = ConnectionManager()


class NotificationService:
    """Service de notifications temps réel"""
    
    @staticmethod
    async def notify_parcel_created(parcel_id: str, parcel_ref: str, created_by: int):
        """Notifier la création d'une parcelle"""
        await manager.broadcast({
            "type": "parcel_created",
            "data": {
                "parcel_id": parcel_id,
                "reference": parcel_ref,
                "created_by": created_by
            },
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_user=created_by)
    
    @staticmethod
    async def notify_parcel_updated(parcel_id: str, parcel_ref: str, updated_by: int):
        """Notifier la modification d'une parcelle"""
        await manager.broadcast({
            "type": "parcel_updated",
            "data": {
                "parcel_id": parcel_id,
                "reference": parcel_ref,
                "updated_by": updated_by
            },
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_user=updated_by)

    @staticmethod
    async def notify_parcel_deleted(parcel_id: str, parcel_ref: str, deleted_by: int):
        """Notifier la suppression d'une parcelle"""
        await manager.broadcast({
            "type": "parcel_deleted",
            "data": {
                "parcel_id": parcel_id,
                "reference": parcel_ref,
                "deleted_by": deleted_by
            },
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_user=deleted_by)
    
    @staticmethod
    async def notify_document_uploaded(doc_id: int, filename: str, parcel_id: int, uploaded_by: int):
        """Notifier l'upload d'un document"""
        await manager.broadcast({
            "type": "document_uploaded",
            "data": {
                "document_id": doc_id,
                "filename": filename,
                "parcel_id": parcel_id,
                "uploaded_by": uploaded_by
            },
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_user=uploaded_by)

    @staticmethod
    async def notify_document_deleted(doc_id: int, filename: str, parcel_id: int, deleted_by: int):
        """Notifier la suppression d'un document"""
        await manager.broadcast({
            "type": "document_deleted",
            "data": {
                "document_id": doc_id,
                "filename": filename,
                "parcel_id": parcel_id,
                "deleted_by": deleted_by
            },
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_user=deleted_by)
    
    @staticmethod
    async def notify_user(user_id: int, notification_type: str, data: Dict[str, Any]):
        """Envoyer une notification à un utilisateur spécifique"""
        await manager.send_to_user({
            "type": notification_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)
    
    @staticmethod
    async def notify_alert(alert_type: str, message: str, severity: str = "info"):
        """Envoyer une alerte système à tous les utilisateurs"""
        await manager.broadcast({
            "type": "system_alert",
            "data": {
                "alert_type": alert_type,
                "message": message,
                "severity": severity
            },
            "timestamp": datetime.utcnow().isoformat()
        })
