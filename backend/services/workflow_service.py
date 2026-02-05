"""
Service de gestion des workflows et approbations
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from backend.core.repository_interfaces import IMutationRepository, IUserRepository, IDocumentRepository
from backend.models.mutation import ParcelMutation
from backend.models.user import User
from backend.models.document import Document


class WorkflowService:
    """
    Service pour la gestion des workflows d'approbation
    """
    
    def __init__(
        self,
        mutation_repository: IMutationRepository,
        user_repository: IUserRepository,
        document_repository: IDocumentRepository
    ):
        self.mutation_repository = mutation_repository
        self.user_repository = user_repository
        self.document_repository = document_repository

    def get_pending_workflows(self, user_id: str) -> List[ParcelMutation]:
        """
        Récupère les workflows en attente pour un utilisateur
        """
        # Récupérer les mutations en attente d'approbation par l'utilisateur
        pending_mutations = self.mutation_repository.get_mutations_for_user(user_id)
        # Filtrer celles qui sont en attente d'approbation
        return [m for m in pending_mutations if m.status in ['pending', 'submitted', 'under_review']]

    def get_user_workflows(self, user_id: str, status: Optional[str] = None) -> List[ParcelMutation]:
        """
        Récupère les workflows initiés par un utilisateur
        """
        filters = {'initiated_by_user_id': user_id}
        if status:
            filters['status'] = status

        user_mutations = self.mutation_repository.search(filters)
        return user_mutations

    def get_workflows_by_type(self, workflow_type: str, status: Optional[str] = None) -> List[ParcelMutation]:
        """
        Récupère les workflows par type
        """
        filters = {'mutation_type': workflow_type}
        if status:
            filters['status'] = status

        mutations = self.mutation_repository.search(filters)
        return mutations

    def submit_approval(self, approval_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Soumet une approbation pour une étape de workflow
        """
        mutation_id = approval_request['mutation_id']
        action = approval_request['action']  # 'approve' or 'reject'
        comment = approval_request.get('comment', '')
        approver_id = approval_request['approver_id']

        # Récupérer la mutation
        mutation = self.mutation_repository.get_by_id(mutation_id)
        if not mutation:
            return {'success': False, 'error': 'Mutation non trouvée'}

        # Vérifier que l'utilisateur est autorisé à approuver
        if not self._is_approver_authorized(mutation, approver_id):
            return {'success': False, 'error': 'Utilisateur non autorisé à approuver cette mutation'}

        # Mettre à jour le statut de la mutation selon l'action
        if action == 'approve':
            # Passer à l'étape suivante ou compléter
            result = self._approve_mutation_step(mutation, approver_id, comment)
        elif action == 'reject':
            # Rejeter la mutation
            result = self._reject_mutation(mutation, approver_id, comment)
        else:
            return {'success': False, 'error': 'Action non valide'}

        return result

    def add_comment(self, mutation_id: str, step_id: str, comment: str) -> Dict[str, Any]:
        """
        Ajoute un commentaire à une étape de workflow
        """
        mutation = self.mutation_repository.get_by_id(mutation_id)
        if not mutation:
            return {'success': False, 'error': 'Mutation non trouvée'}
        
        # Ajouter le commentaire à l'historique de la mutation
        self._add_comment_to_mutation_history(mutation, step_id, comment)
        
        return {'success': True, 'message': 'Commentaire ajouté avec succès'}

    def cancel_workflow(self, mutation_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Annule un workflow
        """
        mutation = self.mutation_repository.get_by_id(mutation_id)
        if not mutation:
            return {'success': False, 'error': 'Mutation non trouvée'}
        
        # Seul l'utilisateur qui a initié la mutation peut l'annuler (ou un admin)
        # Pour l'instant, on autorise l'annulation
        mutation.status = 'cancelled'
        mutation.updated_at = datetime.now()
        if reason:
            mutation.cancellation_reason = reason
        
        updated_mutation = self.mutation_repository.update(mutation_id, mutation)
        
        return {
            'success': True,
            'mutation': self._mutation_to_dict(updated_mutation),
            'message': 'Mutation annulée avec succès'
        }

    def get_possible_approvers(self, workflow_type: str) -> List[Dict[str, Any]]:
        """
        Récupère les approbateurs possibles pour un type de workflow
        """
        # Selon le type de workflow, récupérer les utilisateurs avec les rôles appropriés
        required_roles = self._get_required_roles_for_workflow(workflow_type)
        
        users = self.user_repository.get_by_roles(required_roles)
        
        return [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value if hasattr(user.role, 'value') else str(user.role),
                'full_name': f"{user.first_name} {user.last_name}".strip() or user.username
            }
            for user in users
        ]

    def get_workflow_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques des workflows
        """
        total_mutations = self.mutation_repository.count({})
        pending_mutations = self.mutation_repository.count({'status': 'pending'})
        approved_mutations = self.mutation_repository.count({'status': 'approved'})
        rejected_mutations = self.mutation_repository.count({'status': 'rejected'})
        completed_mutations = self.mutation_repository.count({'status': 'completed'})
        cancelled_mutations = self.mutation_repository.count({'status': 'cancelled'})
        
        # Calculer les pourcentages
        total_with_status = pending_mutations + approved_mutations + rejected_mutations + completed_mutations + cancelled_mutations
        pending_percentage = (pending_mutations / total_with_status * 100) if total_with_status > 0 else 0
        approved_percentage = (approved_mutations / total_with_status * 100) if total_with_status > 0 else 0
        rejected_percentage = (rejected_mutations / total_with_status * 100) if total_with_status > 0 else 0
        completed_percentage = (completed_mutations / total_with_status * 100) if total_with_status > 0 else 0
        cancelled_percentage = (cancelled_mutations / total_with_status * 100) if total_with_status > 0 else 0
        
        return {
            'total': total_mutations,
            'pending': pending_mutations,
            'approved': approved_mutations,
            'rejected': rejected_mutations,
            'completed': completed_mutations,
            'cancelled': cancelled_mutations,
            'percentages': {
                'pending': round(pending_percentage, 2),
                'approved': round(approved_percentage, 2),
                'rejected': round(rejected_percentage, 2),
                'completed': round(completed_percentage, 2),
                'cancelled': round(cancelled_percentage, 2)
            }
        }

    def get_workflow_history(self, page: int, page_size: int, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère l'historique des workflows
        """
        filters = filters or {}
        filters['page'] = page
        filters['page_size'] = page_size
        
        mutations = self.mutation_repository.search_with_pagination(filters)
        
        return {
            'items': [self._mutation_to_dict(m) for m in mutations['items']],
            'total': mutations['total'],
            'page': mutations['page'],
            'page_size': mutations['page_size'],
            'total_pages': mutations['total_pages']
        }

    def get_overdue_workflows(self) -> List[ParcelMutation]:
        """
        Récupère les workflows en retard
        """
        # Pour l'instant, on récupère les mutations avec un statut 'pending' depuis plus de 30 jours
        thirty_days_ago = datetime.now() - timedelta(days=30)

        overdue_mutations = self.mutation_repository.get_overdue(thirty_days_ago)
        return overdue_mutations

    def _is_approver_authorized(self, mutation: ParcelMutation, user_id: str) -> bool:
        """
        Vérifie si un utilisateur est autorisé à approuver une mutation
        """
        # Pour l'instant, on vérifie simplement si l'utilisateur est admin ou manager
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False

        user_role = user.role.value if hasattr(user.role, 'value') else str(user.role)
        return user_role in ['administrator', 'manager']

    def _approve_mutation_step(self, mutation: ParcelMutation, approver_id: str, comment: str) -> Dict[str, Any]:
        """
        Approuve une étape de mutation
        """
        # Mettre à jour la mutation
        mutation.status = 'approved'  # ou passer à l'étape suivante selon le workflow
        mutation.approved_by_user_id = approver_id
        mutation.approved_at = datetime.now()
        mutation.updated_at = datetime.now()

        # Ajouter le commentaire à l'historique
        self._add_comment_to_mutation_history(mutation, 'approval', comment)

        updated_mutation = self.mutation_repository.update(mutation.id, mutation)

        return {
            'success': True,
            'mutation': self._mutation_to_dict(updated_mutation),
            'message': 'Mutation approuvée avec succès'
        }

    def _reject_mutation(self, mutation: ParcelMutation, approver_id: str, comment: str) -> Dict[str, Any]:
        """
        Rejette une mutation
        """
        mutation.status = 'rejected'
        mutation.approved_by_user_id = approver_id
        mutation.approved_at = datetime.now()
        mutation.rejection_reason = comment
        mutation.updated_at = datetime.now()

        # Ajouter le commentaire à l'historique
        self._add_comment_to_mutation_history(mutation, 'rejection', comment)

        updated_mutation = self.mutation_repository.update(mutation.id, mutation)

        return {
            'success': True,
            'mutation': self._mutation_to_dict(updated_mutation),
            'message': 'Mutation rejetée avec succès'
        }

    def _add_comment_to_mutation_history(self, mutation: ParcelMutation, step: str, comment: str):
        """
        Ajoute un commentaire à l'historique de la mutation
        """
        # Pour l'instant, on ajoute simplement le commentaire à la mutation
        # En production, on aurait une table d'historique dédiée
        pass

    def _get_required_roles_for_workflow(self, workflow_type: str) -> List[str]:
        """
        Récupère les rôles requis pour approuver un type de workflow
        """
        role_requirements = {
            'sale': ['administrator', 'manager'],
            'donation': ['administrator', 'manager'],
            'inheritance': ['administrator', 'manager'],
            'exchange': ['administrator', 'manager'],
            'expropriation': ['administrator'],
            'subdivision': ['administrator', 'manager', 'technician'],
            'merge': ['administrator', 'manager', 'technician'],
            'other': ['administrator', 'manager']
        }

        return role_requirements.get(workflow_type, ['administrator'])

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
            'rejection_reason': mutation.rejection_reason
        }