"""
Interfaces pour le pattern Repository
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session

T = TypeVar('T')


class IRepository(Generic[T], ABC):
    """
    Interface de base pour les repositories
    """
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        """
        Récupère une entité par son ID
        """
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Récupère toutes les entités
        """
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Crée une nouvelle entité
        """
        pass

    @abstractmethod
    def update(self, id: str, entity: T) -> Optional[T]:
        """
        Met à jour une entité existante
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """
        Supprime une entité
        """
        pass

    @abstractmethod
    def search(self, criteria: Dict[str, Any]) -> List[T]:
        """
        Recherche des entités selon des critères
        """
        pass


class IParcelRepository(IRepository):
    """
    Interface spécifique pour le repository des parcelles
    """
    
    @abstractmethod
    def get_by_reference(self, reference: str) -> Optional[T]:
        """
        Récupère une parcelle par sa référence cadastrale
        """
        pass

    @abstractmethod
    def get_by_owner(self, owner_id: str) -> List[T]:
        """
        Récupère les parcelles appartenant à un propriétaire
        """
        pass

    @abstractmethod
    def get_with_filters(self, filters: Dict[str, Any]) -> List[T]:
        """
        Récupère des parcelles avec des filtres complexes
        """
        pass


class IParcelHistoryRepository(IRepository):
    """
    Interface spécifique pour le repository de l'historique des parcelles
    """

    @abstractmethod
    def get_by_parcel_id(self, parcel_id: str) -> List[T]:
        """
        Récupère l'historique d'une parcelle par son ID
        """
        pass

    @abstractmethod
    def delete_by_parcel_id(self, parcel_id: str):
        """
        Supprime l'historique d'une parcelle par son ID
        """
        pass


class IParcelReservationRepository(IRepository):
    """
    Interface spécifique pour le repository des réservations de parcelles
    """

    @abstractmethod
    def get_active_reservation(self, parcel_id: str) -> Optional[T]:
        """
        Récupère la réservation active pour une parcelle
        """
        pass


class IVerificationLogRepository(IRepository):
    """
    Interface spécifique pour le repository des logs de vérification
    """

    @abstractmethod
    def get_by_parcel_id(self, parcel_id: str, limit: int) -> List[T]:
        """
        Récupère les logs de vérification pour une parcelle
        """
        pass

    @abstractmethod
    def get_all_with_limit(self, limit: int = 100) -> List[T]:
        """
        Récupère tous les logs de vérification avec une limite
        """
        pass


class IAlertRepository(IRepository):
    """
    Interface spécifique pour le repository des alertes
    """

    @abstractmethod
    def get_alerts(self, acknowledged: Optional[bool], severity: Optional[str], limit: int) -> List[T]:
        """
        Récupère les alertes avec des filtres
        """
        pass

    @abstractmethod
    def get_alerts_for_parcel(self, parcel_id: str) -> List[T]:
        """
        Récupère les alertes pour une parcelle spécifique
        """
        pass


class IUserRepository(IRepository):
    """
    Interface spécifique pour le repository des utilisateurs
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[T]:
        """
        Récupère un utilisateur par son email
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[T]:
        """
        Récupère un utilisateur par son nom d'utilisateur
        """
        pass


class IRoleRepository(IRepository):
    """
    Interface spécifique pour le repository des rôles
    """

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[T]:
        """
        Récupère un rôle par son nom
        """
        pass


class IAuditLogRepository(IRepository):
    """
    Interface spécifique pour le repository des logs d'audit
    """

    @abstractmethod
    def get_audit_logs(
        self,
        action: str = None,
        entity_type: str = None,
        entity_id: str = None,
        user_id: str = None,
        status: str = None,
        date_from: datetime = None,
        date_to: datetime = None,
        is_sensitive: bool = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Récupère les audit logs avec filtres
        """
        pass

    @abstractmethod
    def get_entity_history(
        self,
        entity_type: str,
        entity_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Récupère l'historique complet d'une entité
        """
        pass
    
    @abstractmethod
    def get_user_actions(
        self,
        user_id: str,
        date_from: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Récupère toutes les actions d'un utilisateur
        """
        pass

    @abstractmethod
    def get_audit_stats(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        """
        Récupère des statistiques sur l'audit
        """
        pass
    
    @abstractmethod
    def search_audit_logs(
        self,
        search_term: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Recherche full-text dans les audit logs
        """
        pass
    
    @abstractmethod
    def get_sensitive_actions(
        self,
        date_from: datetime = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Récupère les actions sensibles (suppressions, modifications critiques)
        """
        pass

    @abstractmethod
    def get_action_statistics(
        self,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> Dict[str, Any]:
        """
        Récupère les statistiques détaillées par type d'action
        """
        pass

    @abstractmethod
    def get_top_users(
        self,
        date_from: datetime = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Récupère les utilisateurs les plus actifs
        """
        pass

    @abstractmethod
    def cleanup_old_logs(self, days_to_keep: int = 365) -> int:
        """
        Supprime les logs anciens (rétention)
        """
        pass


class IMutationRepository(IRepository):
    """
    Interface spécifique pour le repository des mutations
    """

    @abstractmethod
    def get_by_parcel_id(self, parcel_id: str) -> List[T]:
        """
        Récupère les mutations pour une parcelle spécifique
        """
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> List[T]:
        """
        Récupère les mutations par statut
        """
        pass

    @abstractmethod
    def get_by_type(self, mutation_type: str) -> List[T]:
        """
        Récupère les mutations par type
        """
        pass

    @abstractmethod
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[T]:
        """
        Récupère les mutations dans une plage de dates
        """
        pass

    @abstractmethod
    def get_pending_mutations(self) -> List[T]:
        """
        Récupère les mutations en attente de traitement
        """
        pass

    @abstractmethod
    def get_mutations_for_user(self, user_id: str) -> List[T]:
        """
        Récupère les mutations liées à un utilisateur (initiateur ou destinataire)
        """
        pass


class IDocumentRepository(IRepository):
    """
    Interface spécifique pour le repository des documents
    """

    @abstractmethod
    def get_by_parcel_id(self, parcel_id: str) -> List[T]:
        """
        Récupère les documents pour une parcelle spécifique
        """
        pass

    @abstractmethod
    def get_by_type(self, document_type: str) -> List[T]:
        """
        Récupère les documents par type
        """
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: str) -> List[T]:
        """
        Récupère les documents appartenant à un propriétaire
        """
        pass

    @abstractmethod
    def search_by_content(self, search_term: str) -> List[T]:
        """
        Recherche dans le contenu textuel des documents
        """
        pass

    @abstractmethod
    def get_recent_documents(self, limit: int = 10) -> List[T]:
        """
        Récupère les documents récents
        """
        pass

    @abstractmethod
    def get_documents_by_date_range(self, start_date: datetime, end_date: datetime) -> List[T]:
        """
        Récupère les documents dans une plage de dates
        """
        pass

    @abstractmethod
    def get_documents_by_tags(self, tags: List[str]) -> List[T]:
        """
        Récupère les documents par tags
        """
        pass
