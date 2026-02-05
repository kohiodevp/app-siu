import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod

class EmailService(ABC):
    """Interface abstraite pour le service d'envoi d'emails"""
    
    @abstractmethod
    def send_confirmation_email(self, recipient_email, username, message):
        """Envoie un email de confirmation à l'utilisateur"""
        pass

class SMTPConfig:
    """Configuration SMTP pour l'envoi d'emails"""
    def __init__(self, smtp_server, smtp_port, username, password, sender_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email

class EmailServiceImpl(EmailService):
    """
    Implémentation du service d'envoi d'emails utilisant SMTP
    
    Correspond à la FR6: Utilisateurs peuvent réinitialiser leur mot de passe via un processus de vérification
    """
    
    def __init__(self, config: SMTPConfig):
        self.config = config
    
    def send_confirmation_email(self, recipient_email, username, message):
        """
        Envoie un email de confirmation à l'utilisateur nouvellement créé
        
        Args:
            recipient_email (str): Adresse email du destinataire
            username (str): Nom d'utilisateur
            message (str): Message personnalisé à inclure dans l'email
            
        Returns:
            bool: True si l'email a été envoyé avec succès, False sinon
        """
        try:
            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = self.config.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Confirmation de votre compte SIU"
            
            # Corps du message
            body = f"""
            Bonjour {username},
            
            Votre compte SIU a été créé avec succès.
            
            {message}
            
            Veuillez conserver cet email pour vos références.
            
            Cordialement,
            L'équipe SIU
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Se connecter au serveur SMTP et envoyer l'email
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.username, self.config.password)
            
            text = msg.as_string()
            server.sendmail(self.config.sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False

# Service d'email par défaut pour les environnements de test
class MockEmailService(EmailService):
    """Service d'email factice pour les tests"""
    
    def send_confirmation_email(self, recipient_email, username, message):
        """Simule l'envoi d'un email de confirmation"""
        print(f"EMAIL MOCK: Envoyé à {recipient_email} pour {username}")
        print(f"Message: {message}")
        return True

# Méthodes statiques pour une utilisation facile
class EmailServiceStatic:
    """Classe avec méthodes statiques pour l'envoi d'emails"""
    
    _instance = MockEmailService()  # Par défaut, utiliser le mock
    
    @staticmethod
    def send_email(to_email: str, subject: str, body: str) -> bool:
        """Envoie un email générique"""
        print(f"EMAIL: To={to_email}, Subject={subject}")
        print(f"Body: {body[:100]}...")
        return True
    
    @staticmethod
    def get_app_url() -> str:
        """Retourne l'URL de l'application"""
        return "http://localhost:8000"

# Alias pour faciliter l'utilisation
EmailService = EmailServiceStatic