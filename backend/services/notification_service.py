"""
Service de notification pour les mutations de parcelles
"""
from typing import List, Optional
from backend.models.mutation import ParcelMutation, MutationType
from backend.models.user import User
from backend.services.email_service import EmailService

class MutationNotificationService:
    """Service pour envoyer des notifications liées aux mutations"""
    
    @staticmethod
    def notify_mutation_created(mutation: ParcelMutation, creator: User, admins: List[User]):
        """
        Notifie les administrateurs qu'une nouvelle mutation a été créée
        """
        subject = f"Nouvelle demande de mutation - Parcelle {mutation.parcel_id}"
        
        mutation_type_labels = {
            'sale': 'Vente',
            'donation': 'Donation',
            'inheritance': 'Héritage',
            'exchange': 'Échange',
            'expropriation': 'Expropriation',
            'subdivision': 'Subdivision',
            'merge': 'Fusion',
            'other': 'Autre'
        }
        
        type_label = mutation_type_labels.get(mutation.mutation_type.value, mutation.mutation_type.value)
        
        # Nettoyer les données sensibles avant insertion dans le template
        import html
        safe_mutation_id = html.escape(str(mutation.id))
        safe_parcel_id = html.escape(str(mutation.parcel_id))
        safe_creator_username = html.escape(str(creator.username))
        safe_creator_email = html.escape(str(creator.email))
        safe_notes = html.escape(str(mutation.notes)) if mutation.notes else 'Aucune note'
        safe_price = f"{html.escape(str(mutation.price))} FCFA" if mutation.price else 'Non spécifié'

        body = f"""
Bonjour,

Une nouvelle demande de mutation a été créée dans le système backend.

Détails de la mutation:
- ID: {safe_mutation_id}
- Parcelle: {safe_parcel_id}
- Type: {type_label}
- Prix: {safe_price}
- Initié par: {safe_creator_username} ({safe_creator_email})
- Date: {mutation.created_at.strftime('%d/%m/%Y %H:%M')}

Notes: {safe_notes}

Cette demande est en attente d'approbation.

Veuillez vous connecter au système pour examiner et approuver/rejeter cette demande:
{EmailService.get_app_url()}/mutations/{safe_mutation_id}

Cordialement,
Système SIU
"""
        
        # Envoyer à tous les administrateurs
        for admin in admins:
            try:
                EmailService.send_email(
                    to_email=admin.email,
                    subject=subject,
                    body=body
                )
            except Exception as e:
                print(f"Erreur envoi email à {admin.email}: {e}")
    
    @staticmethod
    def notify_mutation_approved(mutation: ParcelMutation, approver: User, creator: User):
        """
        Notifie le créateur que sa mutation a été approuvée
        """
        subject = f"Mutation approuvée - Parcelle {mutation.parcel_id}"
        
        # Nettoyer les données sensibles avant insertion dans le template
        import html
        safe_creator_name = html.escape(str(creator.first_name or creator.username))
        safe_mutation_id = html.escape(str(mutation.id))
        safe_parcel_id = html.escape(str(mutation.parcel_id))
        safe_approver_username = html.escape(str(approver.username))
        safe_approval_date = mutation.approved_at.strftime('%d/%m/%Y %H:%M') if mutation.approved_at else 'N/A'

        body = f"""
Bonjour {safe_creator_name},

Votre demande de mutation a été approuvée.

Détails:
- ID: {safe_mutation_id}
- Parcelle: {safe_parcel_id}
- Approuvée par: {safe_approver_username}
- Date d'approbation: {safe_approval_date}

La mutation est maintenant en attente de complétion.

Voir les détails:
{EmailService.get_app_url()}/mutations/{safe_mutation_id}

Cordialement,
Système SIU
"""
        
        try:
            EmailService.send_email(
                to_email=creator.email,
                subject=subject,
                body=body
            )
        except Exception as e:
            print(f"Erreur envoi email: {e}")
    
    @staticmethod
    def notify_mutation_rejected(mutation: ParcelMutation, rejector: User, creator: User):
        """
        Notifie le créateur que sa mutation a été rejetée
        """
        subject = f"Mutation rejetée - Parcelle {mutation.parcel_id}"
        
        # Nettoyer les données sensibles avant insertion dans le template
        import html
        safe_creator_name = html.escape(str(creator.first_name or creator.username))
        safe_mutation_id = html.escape(str(mutation.id))
        safe_parcel_id = html.escape(str(mutation.parcel_id))
        safe_rejector_username = html.escape(str(rejector.username))
        safe_reason = html.escape(str(mutation.rejection_reason)) if mutation.rejection_reason else 'Aucune raison fournie'

        body = f"""
Bonjour {safe_creator_name},

Votre demande de mutation a été rejetée.

Détails:
- ID: {safe_mutation_id}
- Parcelle: {safe_parcel_id}
- Rejetée par: {safe_rejector_username}
- Raison: {safe_reason}

Si vous pensez qu'il s'agit d'une erreur ou si vous souhaitez plus d'informations,
veuillez contacter un administrateur.

Voir les détails:
{EmailService.get_app_url()}/mutations/{safe_mutation_id}

Cordialement,
Système SIU
"""
        
        try:
            EmailService.send_email(
                to_email=creator.email,
                subject=subject,
                body=body
            )
        except Exception as e:
            print(f"Erreur envoi email: {e}")
    
    @staticmethod
    def notify_mutation_completed(mutation: ParcelMutation, creator: User, affected_owners: List[User]):
        """
        Notifie toutes les parties que la mutation est complétée
        """
        subject = f"Mutation complétée - Parcelle {mutation.parcel_id}"
        
        # Nettoyer les données sensibles avant insertion dans le template
        import html
        safe_parcel_id = html.escape(str(mutation.parcel_id))
        safe_mutation_id = html.escape(str(mutation.id))
        safe_mutation_type = html.escape(str(mutation.mutation_type.value))
        safe_completion_date = mutation.completed_at.strftime('%d/%m/%Y %H:%M') if mutation.completed_at else 'N/A'
        safe_price = f"{html.escape(str(mutation.price))} FCFA" if mutation.price else 'Non spécifié'

        body = f"""
Bonjour,

La mutation de la parcelle {safe_parcel_id} a été complétée avec succès.

Détails:
- ID: {safe_mutation_id}
- Type: {safe_mutation_type}
- Date de complétion: {safe_completion_date}
- Prix: {safe_price}

Le transfert de propriété est maintenant effectif.

Voir les détails:
{EmailService.get_app_url()}/mutations/{safe_mutation_id}

Cordialement,
Système SIU
"""
        
        # Notifier le créateur
        try:
            EmailService.send_email(
                to_email=creator.email,
                subject=subject,
                body=body
            )
        except Exception as e:
            print(f"Erreur envoi email créateur: {e}")
        
        # Notifier les propriétaires affectés
        for owner in affected_owners:
            if hasattr(owner, 'email') and owner.email:
                try:
                    EmailService.send_email(
                        to_email=owner.email,
                        subject=subject,
                        body=body
                    )
                except Exception as e:
                    print(f"Erreur envoi email propriétaire: {e}")
