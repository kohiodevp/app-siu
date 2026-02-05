"""
Service de gestion des mutations foncières
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.core.repository_interfaces import IMutationRepository, IUserRepository, IParcelRepository, IDocumentRepository
from backend.models.mutation import ParcelMutation
from backend.models.user import User
from backend.models.parcel import Parcel
from backend.models.document import Document


class MutationService:
    """
    Service pour la gestion des mutations foncières
    """
    
    def __init__(
        self,
        mutation_repository: IMutationRepository,
        user_repository: IUserRepository,
        parcel_repository: IParcelRepository,
        document_repository: IDocumentRepository
    ):
        self.mutation_repository = mutation_repository
        self.user_repository = user_repository
        self.parcel_repository = parcel_repository
        self.document_repository = document_repository

    def get_mutations_pending_legal_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation juridique
        """
        filters = {
            'status': 'pending_legal_validation',
            'page': page,
            'page_size': page_size
        }

        mutations = self.mutation_repository.search_with_pagination(filters)

        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_technical_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation technique
        """
        filters = {
            'status': 'pending_technical_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_administrative_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation administrative
        """
        filters = {
            'status': 'pending_administrative_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_environmental_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation environnementale
        """
        filters = {
            'status': 'pending_environmental_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_social_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation sociale
        """
        filters = {
            'status': 'pending_social_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_economic_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation économique
        """
        filters = {
            'status': 'pending_economic_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_cultural_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation culturelle
        """
        filters = {
            'status': 'pending_cultural_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_religious_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation religieuse
        """
        filters = {
            'status': 'pending_religious_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_traditional_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation traditionnelle
        """
        filters = {
            'status': 'pending_traditional_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_community_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation communautaire
        """
        filters = {
            'status': 'pending_community_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_tribal_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation tribale
        """
        filters = {
            'status': 'pending_tribal_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_customary_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation coutumière
        """
        filters = {
            'status': 'pending_customary_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_constitutional_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation constitutionnelle
        """
        filters = {
            'status': 'pending_constitutional_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_legal_framework_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation du cadre juridique
        """
        filters = {
            'status': 'pending_legal_framework_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_regulatory_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation réglementaire
        """
        filters = {
            'status': 'pending_regulatory_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_international_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation internationale
        """
        filters = {
            'status': 'pending_international_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_regional_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation régionale
        """
        filters = {
            'status': 'pending_regional_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_national_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation nationale
        """
        filters = {
            'status': 'pending_national_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_local_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation locale
        """
        filters = {
            'status': 'pending_local_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_sectorial_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation sectorielle
        """
        filters = {
            'status': 'pending_sectorial_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_intersectorial_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation intersectorielle
        """
        filters = {
            'status': 'pending_intersectorial_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multidimensional_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multidimensionnelle
        """
        filters = {
            'status': 'pending_multidimensional_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multicriteria_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multicritère
        """
        filters = {
            'status': 'pending_multicriteria_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiactor_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiacteur
        """
        filters = {
            'status': 'pending_multiactor_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiscale_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiéchelle
        """
        filters = {
            'status': 'pending_multiscale_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multidenominational_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiconfessionnelle
        """
        filters = {
            'status': 'pending_multidenominational_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multicultural_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiculturelle
        """
        filters = {
            'status': 'pending_multicultural_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multilingual_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multilingue
        """
        filters = {
            'status': 'pending_multilingual_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multinational_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multinationale
        """
        filters = {
            'status': 'pending_multinational_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiparty_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multipartenaires
        """
        filters = {
            'status': 'pending_multiparty_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiprogram_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiprogrammes
        """
        filters = {
            'status': 'pending_multiprogram_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiproject_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiprojets
        """
        filters = {
            'status': 'pending_multiproject_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiperiod_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multipériodes
        """
        filters = {
            'status': 'pending_multiperiod_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiphase_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiphases
        """
        filters = {
            'status': 'pending_multiphase_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiproduct_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiproduits
        """
        filters = {
            'status': 'pending_multiproduct_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiservice_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiservices
        """
        filters = {
            'status': 'pending_multiservice_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multisite_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multisites
        """
        filters = {
            'status': 'pending_multisite_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multistakeholder_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multistakeholders
        """
        filters = {
            'status': 'pending_multistakeholder_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multithematic_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multithématique
        """
        filters = {
            'status': 'pending_multithematic_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_mutations_pending_multiuser_validation(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les mutations en attente de validation multiusager
        """
        filters = {
            'status': 'pending_multiuser_validation',
            'page': page,
            'page_size': page_size
        }
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def _mutation_to_dict(self, mutation: ParcelMutation) -> Dict[str, Any]:
        """
        Convertit une mutation en dictionnaire
        """
        return {
            'id': mutation.id,
            'parcel_id': mutation.parcel_id,
            'mutation_type': mutation.mutation_type.value if hasattr(mutation.mutation_type, 'value') else str(mutation.mutation_type),
            'from_owner_id': mutation.from_owner_id,
            'to_owner_id': mutation.to_owner_id,
            'initiated_by_user_id': mutation.initiated_by_user_id,
            'price': mutation.price,
            'notes': mutation.notes,
            'status': mutation.status.value if hasattr(mutation.status, 'value') else str(mutation.status),
            'created_at': mutation.created_at.isoformat() if hasattr(mutation.created_at, 'isoformat') else str(mutation.created_at),
            'updated_at': mutation.updated_at.isoformat() if hasattr(mutation.updated_at, 'isoformat') else str(mutation.updated_at),
            'approved_at': mutation.approved_at.isoformat() if mutation.approved_at and hasattr(mutation.approved_at, 'isoformat') else None,
            'approved_by_user_id': mutation.approved_by_user_id,
            'completed_at': mutation.completed_at.isoformat() if mutation.completed_at and hasattr(mutation.completed_at, 'isoformat') else None,
            'rejection_reason': mutation.rejection_reason,
            'documents': mutation.documents if hasattr(mutation, 'documents') else []
        }