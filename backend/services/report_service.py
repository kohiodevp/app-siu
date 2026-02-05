"""
Service de génération de rapports complets
Génère des rapports PDF et Excel pour parcelles, activité, audit
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from .pdf_generator import PDFGenerator
from .excel_service import ExcelService

# Import des modèles nécessaires
from backend.models.document_model import Document
from backend.models.parcel import Parcel
from backend.models.user import User


class ReportService:
    """Service principal de génération de rapports"""

    def __init__(self, db_session: Session):
        self.db = db_session  # This will be a SQLAlchemy session
    
    def generate_parcel_report_pdf(
        self,
        parcel_id: str,
        include_history: bool = True,
        include_documents: bool = True,
        include_map: bool = False,
        include_nearby: bool = True,
        nearby_radius: float = 2.0
    ) -> bytes:
        """
        Génère un rapport PDF complet d'une parcelle
        
        Args:
            parcel_id: ID de la parcelle
            include_history: Inclure l'historique
            include_documents: Inclure la liste des documents
            include_map: Inclure une carte statique
            
        Returns:
            bytes: Contenu du PDF
        """
        from backend.services.audit_service import AuditService
        # Valider que l'ID est un UUID valide pour éviter les injections
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, str(parcel_id)):
            raise ValueError("ID de parcelle invalide")

        # Pour récupérer la parcelle, utiliser directement SQLAlchemy avec le modèle
        from backend.models.parcel import Parcel
        from backend.models.user import User
        
        # Récupérer la parcelle avec ses relations
        parcel = self.db.query(Parcel).filter(Parcel.id == str(parcel_id)).first()

        if not parcel:
            raise ValueError(f"Parcelle {parcel_id} non trouvée")

        # Créer le PDF
        pdf = PDFGenerator(
            title=f"LOTISSEMENT {parcel.commune.upper()} - Extrait cadastral",
            author="SIU System",
            subject=f"extrait détaillé de la parcelle ({parcel.anneeachev})"
        )
     
        # # Section 1: Informations générales
        pdf.add_section("EXTRAIT CADASTRAL")
        
        parcel_info = {
            "PARCELLE": parcel.numparc or "N/A",
            "ILOT": parcel.numlot or "N/A",
            "SUPERFICIE": f"{round(parcel.area)} m²" if parcel.area else "N/A",
            "USAGE": parcel.category or "N/A",
            "SITE": parcel.localite or "N/A",
            "DATE": datetime.now().strftime("%d/%m/%Y"),
        }
        
        pdf.add_key_value_table(parcel_info)
        
     
        # Section 5: Parcelles à proximité
        if include_nearby:
            try:
                from .parcel_service import ParcelService
                from .admin_service import AdminService
                from .availability_service import AvailabilityService
                from .email_service import MockEmailService
                from backend.infrastructure.repositories.parcel_repository import SqlParcelRepository
                from backend.infrastructure.repositories.parcel_history_repository import SqlParcelHistoryRepository
                from backend.infrastructure.repositories.user_repository import SqlUserRepository
                from backend.infrastructure.repositories.role_repository import SqlRoleRepository
                from backend.infrastructure.repositories.parcel_reservation_repository import SqlParcelReservationRepository
                from backend.infrastructure.repositories.verification_log_repository import SqlVerificationLogRepository
                
                # Créer une instance du service de parcelle pour obtenir les parcelles à proximité
                parcel_repo = SqlParcelRepository(self.db)
                history_repo = SqlParcelHistoryRepository(self.db)
                user_repo = SqlUserRepository(self.db)
                role_repo = SqlRoleRepository(self.db)
                reservation_repo = SqlParcelReservationRepository(self.db)
                verification_repo = SqlVerificationLogRepository(self.db)
                
                # Créer les services avec les dépendances nécessaires
                from .alert_service import AlertService
                from backend.infrastructure.repositories.alert_repository import SqlAlertRepository
                
                email_service = MockEmailService()  # Utiliser le service d'email factice
                alert_repo = SqlAlertRepository(self.db)
                alert_service = AlertService(alert_repo)
                admin_service = AdminService(user_repo, role_repo, email_service)
                availability_service = AvailabilityService(parcel_repo, reservation_repo, verification_repo, admin_service, alert_service)
                
                parcel_service = ParcelService(
                    parcel_repository=parcel_repo,
                    parcel_history_repository=history_repo,
                    admin_service=admin_service,
                    availability_service=availability_service
                )
                
                # Récupérer les parcelles à proximité (rayon configurable)
                # Pour la section du rapport, utiliser le rayon spécifié
                # nearby_parcels = parcel_service.get_nearby_parcels(parcel_id, radius_km=nearby_radius)
                
                # if nearby_parcels:
                #     # pdf.add_section(f"5. Parcelles à Proximité ({len(nearby_parcels)} trouvées dans un rayon de {nearby_radius} km)")
                    
                #     # Tableau des parcelles à proximité
                #     # nearby_data = [["Référence", "Adresse", "Distance (km)", "Superficie", "Catégorie"]]
                #     # for nearby_parcel in nearby_parcels[:15]:  # Limiter à 15 pour le rapport
                #     #     nearby_data.append([
                #     #         nearby_parcel.get('reference_cadastrale', 'N/A'),
                #     #         nearby_parcel.get('address', 'N/A')[0:30] + "..." if len(str(nearby_parcel.get('address', 'N/A'))) > 30 else nearby_parcel.get('address', 'N/A'),
                #     #         f"{nearby_parcel.get('distance_km', 0):.3f}",
                #     #         f"{nearby_parcel.get('area', 0):.2f} m²",
                #     #         nearby_parcel.get('category', 'N/A')
                #     #     ])
                    
                #     # pdf.add_table(nearby_data, header_row=True, style='striped')
                    
                #     # Résumé statistique
                #     if len(nearby_parcels) > 0:
                #         total_area = sum(p.get('area', 0) for p in nearby_parcels)
                #         categories = [p.get('category', 'N/A') for p in nearby_parcels]
                #         unique_categories = list(set(categories))
                        
                #         summary_data = {
                #             "Total parcelles à proximité": len(nearby_parcels),
                #             "Superficie totale": f"{total_area:.2f} m²",
                #             "Catégories uniques": ", ".join(unique_categories),
                #             "Distance moyenne": f"{sum(p.get('distance_km', 0) for p in nearby_parcels) / len(nearby_parcels):.3f} km"
                #         }
                        
                #         pdf.add_paragraph("<b>Résumé des parcelles à proximité:</b>")
                #         pdf.add_key_value_table(summary_data)
                # else:
                #     pdf.add_section("5. Parcelles à Proximité")
                #     pdf.add_paragraph(f"Aucune autre parcelle n'a été trouvée dans un rayon de {nearby_radius} km.")
                    
            except Exception as e:
                print(f"Erreur lors de l'ajout des parcelles à proximité: {str(e)}")
                # Ne pas ajouter la section si une erreur survient

        # Section 6: Carte de la parcelle (si demandé)
        if include_map:
            try:
                if parcel.coordinates_lat and parcel.coordinates_lng:
                    # pdf.add_section("6. Localisation Géographique")

                    # Calculer les coordonnées à partir de la géométrie si disponible
                    center_lat = float(parcel.coordinates_lat)
                    center_lon = float(parcel.coordinates_lng)
                    
                    # Si la géométrie est disponible, recalculer le centroïde
                    if parcel.geometry:
                        try:
                            import json
                            geom_data = json.loads(json.dumps(parcel.geometry)) if isinstance(parcel.geometry, str) else parcel.geometry
                            
                            if geom_data and 'coordinates' in geom_data:
                                coords = geom_data['coordinates']
                                
                                if geom_data['type'] == 'Polygon':
                                    # Calculer le centroïde du polygone principal
                                    all_coords = []
                                    for poly_coords in coords:
                                        if poly_coords:
                                            all_coords.extend([(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2])
                                    
                                    if all_coords:
                                        center_lon = sum(coord[0] for coord in all_coords) / len(all_coords)
                                        center_lat = sum(coord[1] for coord in all_coords) / len(all_coords)
                                        
                                elif geom_data['type'] == 'MultiPolygon':
                                    # Calculer le centroïde de tous les polygones
                                    all_coords = []
                                    for polygon in coords:
                                        for poly_coords in polygon:
                                            if poly_coords:
                                                all_coords.extend([(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2])
                                    
                                    if all_coords:
                                        center_lon = sum(coord[0] for coord in all_coords) / len(all_coords)
                                        center_lat = sum(coord[1] for coord in all_coords) / len(all_coords)
                        except Exception as e:
                            print(f"Erreur lors du calcul du centroïde à partir de la géométrie: {str(e)}")
                            # Garder les coordonnées par défaut si la géométrie est invalide
                            pass

                    # Ajouter les coordonnées GPS (calculées à partir de la géométrie si disponible)
                    # coords_info = {
                    #     "Latitude": str(center_lat),
                    #     "Longitude": str(center_lon)
                    # }
                    # pdf.add_key_value_table(coords_info)

                    # Générer et ajouter une image de carte
                    import matplotlib
                    matplotlib.use('Agg')  # Utiliser un backend non interactif
                    from io import BytesIO
                    import matplotlib.pyplot as plt
                    from matplotlib.patches import Polygon
                    import json

                    # Créer une figure matplotlib pour la carte (ajustée à la largeur A4)
                    # La largeur A4 est d'environ 8.27 pouces, on laisse un peu de marge
                    fig, ax = plt.subplots(figsize=(8.27, 6))

                    # Dessiner un point pour la parcelle principale
                    ax.plot(center_lon, center_lat, 'ro', markersize=10, label='Parcelle cible')

                    # Récupérer les parcelles à proximité via le service de parcelle
                    from .parcel_service import ParcelService
                    from .admin_service import AdminService
                    from .availability_service import AvailabilityService
                    from backend.infrastructure.repositories.parcel_repository import SqlParcelRepository
                    from backend.infrastructure.repositories.parcel_history_repository import SqlParcelHistoryRepository
                    
                    # Créer une instance du service de parcelle pour obtenir les parcelles à proximité
                    # Pour cela, nous devons créer les dépendances nécessaires
                    parcel_repo = SqlParcelRepository(self.db)
                    history_repo = SqlParcelHistoryRepository(self.db)
                    
                    # On récupère les services via les repositories nécessaires
                    try:
                        from .email_service import MockEmailService
                        from backend.infrastructure.repositories.user_repository import SqlUserRepository
                        from backend.infrastructure.repositories.role_repository import SqlRoleRepository
                        from backend.infrastructure.repositories.parcel_reservation_repository import SqlParcelReservationRepository
                        from backend.infrastructure.repositories.verification_log_repository import SqlVerificationLogRepository
                        
                        user_repo = SqlUserRepository(self.db)
                        role_repo = SqlRoleRepository(self.db)
                        reservation_repo = SqlParcelReservationRepository(self.db)
                        verification_repo = SqlVerificationLogRepository(self.db)
                        
                        # Créer les services avec les dépendances nécessaires
                        from .alert_service import AlertService
                        from backend.infrastructure.repositories.alert_repository import SqlAlertRepository
                        
                        email_service = MockEmailService()  # Utiliser le service d'email factice
                        alert_repo = SqlAlertRepository(self.db)
                        alert_service = AlertService(alert_repo)
                        admin_service = AdminService(user_repo, role_repo, email_service)
                        availability_service = AvailabilityService(parcel_repo, reservation_repo, verification_repo, admin_service, alert_service)
                        
                        parcel_service = ParcelService(
                            parcel_repository=parcel_repo,
                            parcel_history_repository=history_repo,
                            admin_service=admin_service,
                            availability_service=availability_service
                        )
                        
                        # Récupérer les parcelles à proximité (rayon fixé à 500m pour la carte)
                        nearby_parcels = parcel_service.get_nearby_parcels(parcel.id, radius_km=0.5)

                        # Dessiner les parcelles à proximité sur la carte
                        if nearby_parcels:
                            ax.plot(
                                [], [], 'bo', markersize=6, alpha=0.6, label='Parcelles à proximité'
                            )  # Légende vide pour la légende
                            
                            # Dessiner les parcelles à proximité avec des couleurs basées sur la distance
                            # Trier les parcelles par distance pour une meilleure visualisation
                            sorted_nearby = sorted(nearby_parcels[:500], key=lambda p: p['distance_km'])  # Limiter à 10 parcelles
                            
                            # Dessiner les parcelles à proximité avec leurs formes polygonales
                            for i, nearby_parcel in enumerate(sorted_nearby):
                                # Déterminer la couleur basée sur la distance (rouge pour proche, orange/jaune pour éloigné)
                                distance_ratio = i / max(len(sorted_nearby)-1, 1)  # Ratio de 0 à 1 si plus d'une parcelle
                                
                                if len(sorted_nearby) == 1:
                                    color = 'red'  # Si une seule parcelle, la montrer en rouge
                                elif distance_ratio < 0.33:
                                    color = 'red'      # Très proche
                                elif distance_ratio < 0.66:
                                    color = 'orange'   # Moyennement proche
                                else:
                                    color = 'yellow'   # Loin (relativement au rayon)

                                # Dessiner la forme polygonale de la parcelle si disponible
                                if nearby_parcel.get('geometry'):
                                    try:
                                        import json
                                        geom_data = json.loads(json.dumps(nearby_parcel['geometry'])) if isinstance(nearby_parcel['geometry'], str) else nearby_parcel['geometry']
                                        
                                        if geom_data and 'coordinates' in geom_data:
                                            coords = geom_data['coordinates']

                                            if geom_data['type'] == 'Polygon':
                                                # Dessiner le polygone de la parcelle à proximité
                                                for poly_coords in coords:
                                                    if poly_coords:
                                                        poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
                                                        if len(poly_array) > 0:
                                                            poly = Polygon(poly_array, closed=True, fill=True, facecolor=color, edgecolor='black', alpha=0.3)
                                                            ax.add_patch(poly)

                                            elif geom_data['type'] == 'MultiPolygon':
                                                # Dessiner les multipolygones
                                                for polygon in coords:
                                                    for poly_coords in polygon:
                                                        if poly_coords:
                                                            poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
                                                            if len(poly_array) > 0:
                                                                poly = Polygon(poly_array, closed=True, fill=True, facecolor=color, edgecolor='black', alpha=0.3)
                                                                ax.add_patch(poly)
                                    except Exception as e:
                                        print(f"Erreur lors du dessin de la géométrie de la parcelle à proximité: {str(e)}")
                                        # Si la géométrie est invalide, dessiner un point à la place
                                        ax.plot(
                                            float(nearby_parcel['coordinates']['lng']),
                                            float(nearby_parcel['coordinates']['lat']),
                                            'o',
                                            markersize=5,
                                            color=color,
                                            alpha=0.7
                                        )
                                else:
                                    # Si aucune géométrie n'est disponible, dessiner un point
                                    ax.plot(
                                        float(nearby_parcel['coordinates']['lng']),
                                        float(nearby_parcel['coordinates']['lat']),
                                        'o',
                                        markersize=5,
                                        color=color,
                                        alpha=0.7
                                    )
                                
                            # Ajouter une légende pour les distances
                            if len(sorted_nearby) > 1:
                                ax.plot([], [], 'ro', markersize=6, alpha=0.7, label='Très proche')
                                ax.plot([], [], 'yo', markersize=6, alpha=0.7, label='Moyennement proche')
                                ax.plot([], [], 'go', markersize=6, alpha=0.7, label='Plus éloigné')
                            
                    except Exception as e:
                        print(f"Erreur lors de la récupération des parcelles à proximité: {str(e)}")
                        # Continuer sans les parcelles à proximité si une erreur survient

                    # Si la géométrie est disponible, la dessiner
                    if parcel.geometry:
                        try:
                            geom_data = json.loads(json.dumps(parcel.geometry)) if isinstance(parcel.geometry, str) else parcel.geometry

                            if geom_data and 'coordinates' in geom_data:
                                coords = geom_data['coordinates']

                                if geom_data['type'] == 'Polygon':
                                    # Dessiner le polygone de la parcelle
                                    for poly_coords in coords:
                                        if poly_coords:
                                            poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
                                            if len(poly_array) > 0:
                                                poly = Polygon(poly_array, closed=True, fill=True, facecolor='lightblue', edgecolor='blue', alpha=0.5)
                                                ax.add_patch(poly)

                                                # Calculer le centroïde pour positionner le label
                                                centroid_x = sum(p[0] for p in poly_array) / len(poly_array)
                                                centroid_y = sum(p[1] for p in poly_array) / len(poly_array)
                                                ax.text(centroid_x, centroid_y, 'Parcelle', fontsize=6, ha='center', va='center', fontweight='bold')

                                elif geom_data['type'] == 'MultiPolygon':
                                    # Dessiner les multipolygones
                                    for polygon in coords:
                                        for poly_coords in polygon:
                                            if poly_coords:
                                                poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
                                                if len(poly_array) > 0:
                                                    poly = Polygon(poly_array, closed=True, fill=True, facecolor='lightblue', edgecolor='blue', alpha=0.5)
                                                    ax.add_patch(poly)

                                                    # Calculer le centroïde pour positionner le label
                                                    centroid_x = sum(p[0] for p in poly_array) / len(poly_array)
                                                    centroid_y = sum(p[1] for p in poly_array) / len(poly_array)
                                                    ax.text(centroid_x, centroid_y, 'Parcelle', fontsize=6, ha='center', va='center', fontweight='bold')

                        except Exception as e:
                            print(f"Erreur lors du traitement de la géométrie: {str(e)}")

                    # Configurer l'affichage de la carte
                    ax.set_xlabel('Longitude')
                    ax.set_ylabel('Latitude')
                    title = f'Localisation de la parcelle {parcel.reference_cadastrale or parcel.id}'
                    ax.set_title(title)
                    ax.grid(True, linestyle='--', alpha=0.6)
                    
                    # Ajouter un cercle pour représenter le rayon de recherche (fixé à 500m pour les parcelles à proximité)
                    import numpy as np
                    circle_points = 100
                    theta = np.linspace(0, 2*np.pi, circle_points)
                    
                    # Convertir le rayon de km en degrés approximatifs (1 degré ≈ 111 km)
                    radius_deg = 0.5 / 111.0  # 500 mètres = 0.5 km
                    
                    circle_x = center_lon + radius_deg * np.cos(theta)
                    circle_y = center_lat + radius_deg * np.sin(theta)
                    
                    ax.plot(circle_x, circle_y, '--', color='gray', linewidth=1, alpha=0.7, label='Rayon de 500m')
                    
                    # Élargir le cadre de la carte pour montrer un contexte plus large (zoom réduit à 250m pour plus de détails)
                    extent_deg = 0.25 / 111.0  # 250 mètres = 0.25 km en degrés pour un zoom plus serré
                    ax.set_xlim(center_lon - extent_deg, center_lon + extent_deg)
                    ax.set_ylim(center_lat - extent_deg, center_lat + extent_deg)
                    
                    ax.legend()

                    # Sauvegarder la figure dans un buffer
                    img_buffer = BytesIO()
                    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                    img_buffer.seek(0)

                    # Ajouter l'image au PDF (ajustée à la largeur A4)
                    # La largeur d'une page PDF A4 est d'environ 595 points, avec des marges, on utilise environ 530 points
                    pdf.add_image(img_buffer, width=555, height=520)

                    # Fermer la figure pour libérer la mémoire
                    plt.close(fig)

            except Exception as e:
                # En cas d'erreur avec la carte, on continue sans
                print(f"Erreur lors de l'ajout de la carte: {str(e)}")
                import traceback
                traceback.print_exc()
                pass

        # Générer le PDF
        return pdf.build()
    
    
    # def generate_parcel_report_pdf(
    #     self,
    #     parcel_id: str,
    #     include_history: bool = True,
    #     include_documents: bool = True,
    #     include_map: bool = False,
    #     include_nearby: bool = True,
    #     nearby_radius: float = 2.0
    # ) -> bytes:
    #     """
    #     Génère un rapport PDF complet d'une parcelle
        
    #     Args:
    #         parcel_id: ID de la parcelle
    #         include_history: Inclure l'historique
    #         include_documents: Inclure la liste des documents
    #         include_map: Inclure une carte statique
            
    #     Returns:
    #         bytes: Contenu du PDF
    #     """
    #     from backend.services.audit_service import AuditService
    #     # Valider que l'ID est un UUID valide pour éviter les injections
    #     import re
    #     uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    #     if not re.match(uuid_pattern, str(parcel_id)):
    #         raise ValueError("ID de parcelle invalide")

    #     # Pour récupérer la parcelle, utiliser directement SQLAlchemy avec le modèle
    #     from backend.models.parcel import Parcel
    #     from backend.models.user import User
        
    #     # Récupérer la parcelle avec ses relations
    #     parcel = self.db.query(Parcel).filter(Parcel.id == str(parcel_id)).first()

    #     if not parcel:
    #         raise ValueError(f"Parcelle {parcel_id} non trouvée")

    #     # Créer le PDF
    #     pdf = PDFGenerator(
    #         title=f"Rapport Parcelle #{parcel.reference_cadastrale}",
    #         author="SIU System",
    #         subject=f"Rapport détaillé de la parcelle {parcel.reference_cadastrale}"
    #     )
        
    #     # Métadonnées
    #     pdf.add_metadata_section({
    #         "Date de génération": datetime.now().strftime("%d/%m/%Y %H:%M"),
    #         "Parcelle": parcel.reference_cadastrale,
    #         "Statut": parcel.status
    #     })
        
    #     # Titre
    #     pdf.add_title(f"Rapport de Parcelle")
    #     pdf.add_subtitle(f"Référence cadastrale : {parcel.reference_cadastrale}")
        
    #     # Section 1: Informations générales
    #     pdf.add_section("1. Informations Générales")
        
    #     parcel_info = {
    #         "Référence cadastrale": parcel.reference_cadastrale or "N/A",
    #         "Adresse": parcel.address or "N/A",
    #         "Superficie": f"{parcel.area} m²" if parcel.area else "N/A",
    #         "Zone": parcel.zone or "N/A",
    #         "Catégorie": parcel.category or "N/A",
    #         "Statut": parcel.status or "N/A",
    #         "Date de création": parcel.created_at.strftime("%d/%m/%Y") if parcel.created_at else "N/A",
    #     }
        
    #     if parcel.owner:
    #         # Assurez-vous que l'attribut full_name existe dans le modèle User
    #         # Sinon, utilisez first_name et last_name
    #         owner_name = f"{parcel.owner.first_name or ''} {parcel.owner.last_name or ''}".strip()
    #         if not owner_name:
    #             owner_name = parcel.owner.username
    #         parcel_info["Propriétaire"] = owner_name

    #     if parcel.coordinates_lat and parcel.coordinates_lng:
    #         parcel_info["Coordonnées"] = f"{parcel.coordinates_lat}, {parcel.coordinates_lng}"
        
    #     pdf.add_key_value_table(parcel_info)
        
    #     # Section 2: Description
    #     if parcel.description:
    #         pdf.add_section("2. Description")
    #         pdf.add_paragraph(parcel.description)
        
    #     # Section 3: Documents
    #     if include_documents:
    #         documents = self.db.query(Document).filter(
    #             Document.parcel_id == str(parcel_id),
    #             Document.deleted == False  # Convertir en booléen pour comparaison
    #         ).all()

    #         if documents:
    #             pdf.add_section(f"3. Documents Associés ({len(documents)})")

    #             doc_data = [["Titre", "Type", "Date", "Statut"]]
    #             for doc in documents:
    #                 # Convertir deleted en booléen pour comparaison
    #                 is_deleted = bool(doc.deleted) if isinstance(doc.deleted, int) else doc.deleted
    #                 doc_data.append([
    #                     doc.original_filename,  # Utiliser original_filename au lieu de title
    #                     doc.document_type,
    #                     doc.uploaded_at.strftime("%d/%m/%Y") if doc.uploaded_at else "N/A",
    #                     "Validé" if not is_deleted else "En attente"  # Utiliser le statut deleted pour simplifier
    #                 ])

    #             pdf.add_table(doc_data, header_row=True, style='striped')
        
    #     # Section 4: Historique
    #     if include_history:
    #         from .audit_service import AuditService
    #         from backend.infrastructure.repositories.audit_log_repository import SqlAuditLogRepository
            
    #         # Créer le repository d'audit et le service
    #         audit_repo = SqlAuditLogRepository(self.db)
    #         audit_service = AuditService(audit_repo)
            
    #         history = audit_service.get_entity_history('parcel', str(parcel_id), limit=20)

    #         if history:
    #             pdf.add_section(f"4. Historique des Modifications ({len(history)})")

    #             history_data = [["Date", "Action", "Utilisateur", "Détails"]]
    #             for log in history:
    #                 details = log.get('validation_comment', '') or ''
    #                 if log.get('changes'):
    #                     changes_count = len(log['changes'])
    #                     details = f"{changes_count} champ(s) modifié(s)"

    #                 history_data.append([
    #                     datetime.fromisoformat(log['timestamp']).strftime("%d/%m/%Y %H:%M"),
    #                     log.get('action', 'N/A'),
    #                     log.get('username', 'Système'),
    #                     details
    #                 ])

    #             pdf.add_table(history_data, header_row=True, style='striped')

    #     # Section 5: Parcelles à proximité
    #     if include_nearby:
    #         try:
    #             from .parcel_service import ParcelService
    #             from .admin_service import AdminService
    #             from .availability_service import AvailabilityService
    #             from .email_service import MockEmailService
    #             from backend.infrastructure.repositories.parcel_repository import SqlParcelRepository
    #             from backend.infrastructure.repositories.parcel_history_repository import SqlParcelHistoryRepository
    #             from backend.infrastructure.repositories.user_repository import SqlUserRepository
    #             from backend.infrastructure.repositories.role_repository import SqlRoleRepository
    #             from backend.infrastructure.repositories.parcel_reservation_repository import SqlParcelReservationRepository
    #             from backend.infrastructure.repositories.verification_log_repository import SqlVerificationLogRepository
                
    #             # Créer une instance du service de parcelle pour obtenir les parcelles à proximité
    #             parcel_repo = SqlParcelRepository(self.db)
    #             history_repo = SqlParcelHistoryRepository(self.db)
    #             user_repo = SqlUserRepository(self.db)
    #             role_repo = SqlRoleRepository(self.db)
    #             reservation_repo = SqlParcelReservationRepository(self.db)
    #             verification_repo = SqlVerificationLogRepository(self.db)
                
    #             # Créer les services avec les dépendances nécessaires
    #             from .alert_service import AlertService
    #             from backend.infrastructure.repositories.alert_repository import SqlAlertRepository
                
    #             email_service = MockEmailService()  # Utiliser le service d'email factice
    #             alert_repo = SqlAlertRepository(self.db)
    #             alert_service = AlertService(alert_repo)
    #             admin_service = AdminService(user_repo, role_repo, email_service)
    #             availability_service = AvailabilityService(parcel_repo, reservation_repo, verification_repo, admin_service, alert_service)
                
    #             parcel_service = ParcelService(
    #                 parcel_repository=parcel_repo,
    #                 parcel_history_repository=history_repo,
    #                 admin_service=admin_service,
    #                 availability_service=availability_service
    #             )
                
    #             # Récupérer les parcelles à proximité (rayon configurable)
    #             # Pour la section du rapport, utiliser le rayon spécifié
    #             nearby_parcels = parcel_service.get_nearby_parcels(parcel_id, radius_km=nearby_radius)
                
    #             if nearby_parcels:
    #                 pdf.add_section(f"5. Parcelles à Proximité ({len(nearby_parcels)} trouvées dans un rayon de {nearby_radius} km)")
                    
    #                 # Tableau des parcelles à proximité
    #                 nearby_data = [["Référence", "Adresse", "Distance (km)", "Superficie", "Catégorie"]]
    #                 for nearby_parcel in nearby_parcels[:15]:  # Limiter à 15 pour le rapport
    #                     nearby_data.append([
    #                         nearby_parcel.get('reference_cadastrale', 'N/A'),
    #                         nearby_parcel.get('address', 'N/A')[0:30] + "..." if len(str(nearby_parcel.get('address', 'N/A'))) > 30 else nearby_parcel.get('address', 'N/A'),
    #                         f"{nearby_parcel.get('distance_km', 0):.3f}",
    #                         f"{nearby_parcel.get('area', 0):.2f} m²",
    #                         nearby_parcel.get('category', 'N/A')
    #                     ])
                    
    #                 pdf.add_table(nearby_data, header_row=True, style='striped')
                    
    #                 # Résumé statistique
    #                 if len(nearby_parcels) > 0:
    #                     total_area = sum(p.get('area', 0) for p in nearby_parcels)
    #                     categories = [p.get('category', 'N/A') for p in nearby_parcels]
    #                     unique_categories = list(set(categories))
                        
    #                     summary_data = {
    #                         "Total parcelles à proximité": len(nearby_parcels),
    #                         "Superficie totale": f"{total_area:.2f} m²",
    #                         "Catégories uniques": ", ".join(unique_categories),
    #                         "Distance moyenne": f"{sum(p.get('distance_km', 0) for p in nearby_parcels) / len(nearby_parcels):.3f} km"
    #                     }
                        
    #                     pdf.add_paragraph("<b>Résumé des parcelles à proximité:</b>")
    #                     pdf.add_key_value_table(summary_data)
    #             else:
    #                 pdf.add_section("5. Parcelles à Proximité")
    #                 pdf.add_paragraph(f"Aucune autre parcelle n'a été trouvée dans un rayon de {nearby_radius} km.")
                    
    #         except Exception as e:
    #             print(f"Erreur lors de l'ajout des parcelles à proximité: {str(e)}")
    #             # Ne pas ajouter la section si une erreur survient

    #     # Section 6: Carte de la parcelle (si demandé)
    #     if include_map:
    #         try:
    #             if parcel.coordinates_lat and parcel.coordinates_lng:
    #                 pdf.add_section("6. Localisation Géographique")

    #                 # Calculer les coordonnées à partir de la géométrie si disponible
    #                 center_lat = float(parcel.coordinates_lat)
    #                 center_lon = float(parcel.coordinates_lng)
                    
    #                 # Si la géométrie est disponible, recalculer le centroïde
    #                 if parcel.geometry:
    #                     try:
    #                         import json
    #                         geom_data = json.loads(json.dumps(parcel.geometry)) if isinstance(parcel.geometry, str) else parcel.geometry
                            
    #                         if geom_data and 'coordinates' in geom_data:
    #                             coords = geom_data['coordinates']
                                
    #                             if geom_data['type'] == 'Polygon':
    #                                 # Calculer le centroïde du polygone principal
    #                                 all_coords = []
    #                                 for poly_coords in coords:
    #                                     if poly_coords:
    #                                         all_coords.extend([(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2])
                                    
    #                                 if all_coords:
    #                                     center_lon = sum(coord[0] for coord in all_coords) / len(all_coords)
    #                                     center_lat = sum(coord[1] for coord in all_coords) / len(all_coords)
                                        
    #                             elif geom_data['type'] == 'MultiPolygon':
    #                                 # Calculer le centroïde de tous les polygones
    #                                 all_coords = []
    #                                 for polygon in coords:
    #                                     for poly_coords in polygon:
    #                                         if poly_coords:
    #                                             all_coords.extend([(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2])
                                    
    #                                 if all_coords:
    #                                     center_lon = sum(coord[0] for coord in all_coords) / len(all_coords)
    #                                     center_lat = sum(coord[1] for coord in all_coords) / len(all_coords)
    #                     except Exception as e:
    #                         print(f"Erreur lors du calcul du centroïde à partir de la géométrie: {str(e)}")
    #                         # Garder les coordonnées par défaut si la géométrie est invalide
    #                         pass

    #                 # Ajouter les coordonnées GPS (calculées à partir de la géométrie si disponible)
    #                 coords_info = {
    #                     "Latitude": str(center_lat),
    #                     "Longitude": str(center_lon)
    #                 }
    #                 pdf.add_key_value_table(coords_info)

    #                 # Générer et ajouter une image de carte
    #                 import matplotlib
    #                 matplotlib.use('Agg')  # Utiliser un backend non interactif
    #                 from io import BytesIO
    #                 import matplotlib.pyplot as plt
    #                 from matplotlib.patches import Polygon
    #                 import json

    #                 # Créer une figure matplotlib pour la carte (ajustée à la largeur A4)
    #                 # La largeur A4 est d'environ 8.27 pouces, on laisse un peu de marge
    #                 fig, ax = plt.subplots(figsize=(7.5, 6))

    #                 # Dessiner un point pour la parcelle principale
    #                 ax.plot(center_lon, center_lat, 'ro', markersize=10, label='Parcelle cible')

    #                 # Récupérer les parcelles à proximité via le service de parcelle
    #                 from .parcel_service import ParcelService
    #                 from .admin_service import AdminService
    #                 from .availability_service import AvailabilityService
    #                 from backend.infrastructure.repositories.parcel_repository import SqlParcelRepository
    #                 from backend.infrastructure.repositories.parcel_history_repository import SqlParcelHistoryRepository
                    
    #                 # Créer une instance du service de parcelle pour obtenir les parcelles à proximité
    #                 # Pour cela, nous devons créer les dépendances nécessaires
    #                 parcel_repo = SqlParcelRepository(self.db)
    #                 history_repo = SqlParcelHistoryRepository(self.db)
                    
    #                 # On récupère les services via les repositories nécessaires
    #                 try:
    #                     from .email_service import MockEmailService
    #                     from backend.infrastructure.repositories.user_repository import SqlUserRepository
    #                     from backend.infrastructure.repositories.role_repository import SqlRoleRepository
    #                     from backend.infrastructure.repositories.parcel_reservation_repository import SqlParcelReservationRepository
    #                     from backend.infrastructure.repositories.verification_log_repository import SqlVerificationLogRepository
                        
    #                     user_repo = SqlUserRepository(self.db)
    #                     role_repo = SqlRoleRepository(self.db)
    #                     reservation_repo = SqlParcelReservationRepository(self.db)
    #                     verification_repo = SqlVerificationLogRepository(self.db)
                        
    #                     # Créer les services avec les dépendances nécessaires
    #                     from .alert_service import AlertService
    #                     from backend.infrastructure.repositories.alert_repository import SqlAlertRepository
                        
    #                     email_service = MockEmailService()  # Utiliser le service d'email factice
    #                     alert_repo = SqlAlertRepository(self.db)
    #                     alert_service = AlertService(alert_repo)
    #                     admin_service = AdminService(user_repo, role_repo, email_service)
    #                     availability_service = AvailabilityService(parcel_repo, reservation_repo, verification_repo, admin_service, alert_service)
                        
    #                     parcel_service = ParcelService(
    #                         parcel_repository=parcel_repo,
    #                         parcel_history_repository=history_repo,
    #                         admin_service=admin_service,
    #                         availability_service=availability_service
    #                     )
                        
    #                     # Récupérer les parcelles à proximité (rayon fixé à 500m pour la carte)
    #                     nearby_parcels = parcel_service.get_nearby_parcels(parcel.id, radius_km=0.5)

    #                     # Dessiner les parcelles à proximité sur la carte
    #                     if nearby_parcels:
    #                         ax.plot(
    #                             [], [], 'bo', markersize=6, alpha=0.6, label='Parcelles à proximité'
    #                         )  # Légende vide pour la légende
                            
    #                         # Dessiner les parcelles à proximité avec des couleurs basées sur la distance
    #                         # Trier les parcelles par distance pour une meilleure visualisation
    #                         sorted_nearby = sorted(nearby_parcels[:100], key=lambda p: p['distance_km'])  # Limiter à 10 parcelles
                            
    #                         # Dessiner les parcelles à proximité avec leurs formes polygonales
    #                         for i, nearby_parcel in enumerate(sorted_nearby):
    #                             # Déterminer la couleur basée sur la distance (rouge pour proche, orange/jaune pour éloigné)
    #                             distance_ratio = i / max(len(sorted_nearby)-1, 1)  # Ratio de 0 à 1 si plus d'une parcelle
                                
    #                             if len(sorted_nearby) == 1:
    #                                 color = 'red'  # Si une seule parcelle, la montrer en rouge
    #                             elif distance_ratio < 0.33:
    #                                 color = 'red'      # Très proche
    #                             elif distance_ratio < 0.66:
    #                                 color = 'orange'   # Moyennement proche
    #                             else:
    #                                 color = 'yellow'   # Loin (relativement au rayon)

    #                             # Dessiner la forme polygonale de la parcelle si disponible
    #                             if nearby_parcel.get('geometry'):
    #                                 try:
    #                                     import json
    #                                     geom_data = json.loads(json.dumps(nearby_parcel['geometry'])) if isinstance(nearby_parcel['geometry'], str) else nearby_parcel['geometry']
                                        
    #                                     if geom_data and 'coordinates' in geom_data:
    #                                         coords = geom_data['coordinates']

    #                                         if geom_data['type'] == 'Polygon':
    #                                             # Dessiner le polygone de la parcelle à proximité
    #                                             for poly_coords in coords:
    #                                                 if poly_coords:
    #                                                     poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
    #                                                     if len(poly_array) > 0:
    #                                                         poly = Polygon(poly_array, closed=True, fill=True, facecolor=color, edgecolor='black', alpha=0.3)
    #                                                         ax.add_patch(poly)

    #                                         elif geom_data['type'] == 'MultiPolygon':
    #                                             # Dessiner les multipolygones
    #                                             for polygon in coords:
    #                                                 for poly_coords in polygon:
    #                                                     if poly_coords:
    #                                                         poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
    #                                                         if len(poly_array) > 0:
    #                                                             poly = Polygon(poly_array, closed=True, fill=True, facecolor=color, edgecolor='black', alpha=0.3)
    #                                                             ax.add_patch(poly)
    #                                 except Exception as e:
    #                                     print(f"Erreur lors du dessin de la géométrie de la parcelle à proximité: {str(e)}")
    #                                     # Si la géométrie est invalide, dessiner un point à la place
    #                                     ax.plot(
    #                                         float(nearby_parcel['coordinates']['lng']),
    #                                         float(nearby_parcel['coordinates']['lat']),
    #                                         'o',
    #                                         markersize=6,
    #                                         color=color,
    #                                         alpha=0.7
    #                                     )
    #                             else:
    #                                 # Si aucune géométrie n'est disponible, dessiner un point
    #                                 ax.plot(
    #                                     float(nearby_parcel['coordinates']['lng']),
    #                                     float(nearby_parcel['coordinates']['lat']),
    #                                     'o',
    #                                     markersize=6,
    #                                     color=color,
    #                                     alpha=0.7
    #                                 )
                                
    #                         # Ajouter une légende pour les distances
    #                         if len(sorted_nearby) > 1:
    #                             ax.plot([], [], 'ro', markersize=6, alpha=0.7, label='Très proche')
    #                             ax.plot([], [], 'yo', markersize=6, alpha=0.7, label='Moyennement proche')
    #                             ax.plot([], [], 'go', markersize=6, alpha=0.7, label='Plus éloigné')
                            
    #                 except Exception as e:
    #                     print(f"Erreur lors de la récupération des parcelles à proximité: {str(e)}")
    #                     # Continuer sans les parcelles à proximité si une erreur survient

    #                 # Si la géométrie est disponible, la dessiner
    #                 if parcel.geometry:
    #                     try:
    #                         geom_data = json.loads(json.dumps(parcel.geometry)) if isinstance(parcel.geometry, str) else parcel.geometry

    #                         if geom_data and 'coordinates' in geom_data:
    #                             coords = geom_data['coordinates']

    #                             if geom_data['type'] == 'Polygon':
    #                                 # Dessiner le polygone de la parcelle
    #                                 for poly_coords in coords:
    #                                     if poly_coords:
    #                                         poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
    #                                         if len(poly_array) > 0:
    #                                             poly = Polygon(poly_array, closed=True, fill=True, facecolor='lightblue', edgecolor='blue', alpha=0.5)
    #                                             ax.add_patch(poly)

    #                                             # Calculer le centroïde pour positionner le label
    #                                             centroid_x = sum(p[0] for p in poly_array) / len(poly_array)
    #                                             centroid_y = sum(p[1] for p in poly_array) / len(poly_array)
    #                                             ax.text(centroid_x, centroid_y, 'Parcelle', fontsize=8, ha='center', va='center', fontweight='bold')

    #                             elif geom_data['type'] == 'MultiPolygon':
    #                                 # Dessiner les multipolygones
    #                                 for polygon in coords:
    #                                     for poly_coords in polygon:
    #                                         if poly_coords:
    #                                             poly_array = [(float(coord[0]), float(coord[1])) for coord in poly_coords if len(coord) >= 2]
    #                                             if len(poly_array) > 0:
    #                                                 poly = Polygon(poly_array, closed=True, fill=True, facecolor='lightblue', edgecolor='blue', alpha=0.5)
    #                                                 ax.add_patch(poly)

    #                                                 # Calculer le centroïde pour positionner le label
    #                                                 centroid_x = sum(p[0] for p in poly_array) / len(poly_array)
    #                                                 centroid_y = sum(p[1] for p in poly_array) / len(poly_array)
    #                                                 ax.text(centroid_x, centroid_y, 'Parcelle', fontsize=8, ha='center', va='center', fontweight='bold')

    #                     except Exception as e:
    #                         print(f"Erreur lors du traitement de la géométrie: {str(e)}")

    #                 # Configurer l'affichage de la carte
    #                 ax.set_xlabel('Longitude')
    #                 ax.set_ylabel('Latitude')
    #                 title = f'Localisation de la parcelle {parcel.reference_cadastrale or parcel.id}'
    #                 ax.set_title(title)
    #                 ax.grid(True, linestyle='--', alpha=0.6)
                    
    #                 # Ajouter un cercle pour représenter le rayon de recherche (fixé à 500m pour les parcelles à proximité)
    #                 import numpy as np
    #                 circle_points = 100
    #                 theta = np.linspace(0, 2*np.pi, circle_points)
                    
    #                 # Convertir le rayon de km en degrés approximatifs (1 degré ≈ 111 km)
    #                 radius_deg = 0.5 / 111.0  # 500 mètres = 0.5 km
                    
    #                 circle_x = center_lon + radius_deg * np.cos(theta)
    #                 circle_y = center_lat + radius_deg * np.sin(theta)
                    
    #                 ax.plot(circle_x, circle_y, '--', color='gray', linewidth=1, alpha=0.7, label='Rayon de 500m')
                    
    #                 # Élargir le cadre de la carte pour montrer un contexte plus large (zoom réduit à 250m pour plus de détails)
    #                 extent_deg = 0.15 / 111.0  # 250 mètres = 0.25 km en degrés pour un zoom plus serré
    #                 ax.set_xlim(center_lon - extent_deg, center_lon + extent_deg)
    #                 ax.set_ylim(center_lat - extent_deg, center_lat + extent_deg)
                    
    #                 ax.legend()

    #                 # Sauvegarder la figure dans un buffer
    #                 img_buffer = BytesIO()
    #                 plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    #                 img_buffer.seek(0)

    #                 # Ajouter l'image au PDF (ajustée à la largeur A4)
    #                 # La largeur d'une page PDF A4 est d'environ 595 points, avec des marges, on utilise environ 530 points
    #                 pdf.add_image(img_buffer, width=500, height=400)

    #                 # Fermer la figure pour libérer la mémoire
    #                 plt.close(fig)

    #         except Exception as e:
    #             # En cas d'erreur avec la carte, on continue sans
    #             print(f"Erreur lors de l'ajout de la carte: {str(e)}")
    #             import traceback
    #             traceback.print_exc()
    #             pass

    #     # Générer le PDF
    #     return pdf.build()
    
    def generate_activity_report_pdf(
        self,
        days: int = 30,
        user_id: Optional[int] = None
    ) -> bytes:
        """
        Génère un rapport d'activité PDF
        
        Args:
            days: Nombre de jours à inclure
            user_id: Filtrer par utilisateur (optionnel)
            
        Returns:
            bytes: Contenu du PDF
        """
        from backend.services.analytics_service import AnalyticsService
        from backend.services.audit_service import AuditService
        
        analytics = AnalyticsService(self.db)
        audit = AuditService(self.db)
        
        # Valider les paramètres d'entrée
        if not isinstance(days, int) or days < 1 or days > 365:
            raise ValueError("Le nombre de jours doit être compris entre 1 et 365")

        if user_id is not None and (not isinstance(user_id, int) or user_id < 1):
            raise ValueError("L'ID utilisateur doit être un entier positif")

        # Créer le PDF
        pdf = PDFGenerator(
            title="Rapport d'Activité",
            author="SIU System",
            subject=f"Rapport d'activité des {days} derniers jours"
        )

        # Métadonnées
        date_from = datetime.utcnow() - timedelta(days=days)
        pdf.add_metadata_section({
            "Période": f"Du {date_from.strftime('%d/%m/%Y')} au {datetime.utcnow().strftime('%d/%m/%Y')}",
            "Durée": f"{days} jours"
        })
        
        pdf.add_title("Rapport d'Activité du Système")
        pdf.add_subtitle(f"Période de {days} jours")
        
        # Stats globales
        pdf.add_section("1. Statistiques Globales")
        
        stats = analytics.get_global_stats()
        if stats:
            stats_data = {
                "Total Parcelles": stats.get('parcels', {}).get('total', 0),
                "Parcelles avec propriétaire": stats.get('parcels', {}).get('with_owner', 0),
                "Total Documents": stats.get('documents', {}).get('total', 0),
                "Documents validés": stats.get('documents', {}).get('validated', 0),
                "Total Utilisateurs": stats.get('users', {}).get('total', 0),
                "Utilisateurs actifs (30j)": stats.get('users', {}).get('active_30d', 0),
            }
            pdf.add_key_value_table(stats_data)
        
        # Actions récentes
        pdf.add_section("2. Actions Récentes")
        
        recent_activity = analytics.get_recent_activity(limit=15)
        if recent_activity:
            activity_data = [["Date", "Action", "Entité", "Utilisateur"]]
            for activity in recent_activity:
                activity_data.append([
                    activity['timestamp'].strftime("%d/%m/%Y %H:%M") if isinstance(activity['timestamp'], datetime) else activity['timestamp'],
                    activity['action'],
                    f"{activity['field'] or 'N/A'}",
                    f"User #{activity['updated_by']}"
                ])
            
            pdf.add_table(activity_data, header_row=True, style='striped')
        
        # Audit stats
        pdf.add_section("3. Statistiques d'Audit")
        
        audit_stats = audit.get_audit_stats(date_from=date_from)
        if audit_stats:
            audit_data = {
                "Total actions": audit_stats.get('total', 0),
                "Actions réussies": audit_stats.get('by_status', {}).get('success', 0),
                "Actions échouées": audit_stats.get('by_status', {}).get('failure', 0),
            }
            pdf.add_key_value_table(audit_data)
            
            # Actions par type
            if audit_stats.get('by_action'):
                pdf.add_paragraph("<b>Répartition par type d'action:</b>")
                action_data = [["Action", "Nombre"]]
                for action, count in audit_stats['by_action'].items():
                    action_data.append([action, str(count)])
                pdf.add_table(action_data, header_row=True)
        
        return pdf.build()
    
    def export_parcels_excel(
        self,
        filters: Dict[str, Any] = None
    ) -> bytes:
        """
        Exporte les parcelles vers Excel
        
        Args:
            filters: Filtres à appliquer
            
        Returns:
            bytes: Contenu du fichier Excel
        """
        from backend.models.parcel import Parcel
        
        # Valider les filtres d'entrée
        if filters:
            if not isinstance(filters, dict):
                raise ValueError("Les filtres doivent être un dictionnaire")

            # Vérifier que seuls les champs autorisés sont présents
            allowed_filters = {'zone', 'status', 'category', 'owner_id'}
            invalid_keys = set(filters.keys()) - allowed_filters
            if invalid_keys:
                raise ValueError(f"Filtres non autorisés: {invalid_keys}")

        query = self.db.query(Parcel)

        # Appliquer les filtres
        if filters:
            if filters.get('zone'):
                # Valider que la zone ne contient pas de caractères spéciaux
                import re
                if not re.match(r'^[a-zA-Z0-9 _-]+$', str(filters['zone'])):
                    raise ValueError("La zone contient des caractères non valides")
                query = query.filter(Parcel.zone == filters['zone'])
            if filters.get('status'):
                # Valider que le statut ne contient pas de caractères spéciaux
                if not re.match(r'^[a-zA-Z0-9 _-]+$', str(filters['status'])):
                    raise ValueError("Le statut contient des caractères non valides")
                query = query.filter(Parcel.status == filters['status'])
        
        parcels = query.all()
        
        # Créer l'Excel
        excel = ExcelService(title="Export Parcelles SIU")
        
        # Convertir en dictionnaires
        parcels_data = []
        for parcel in parcels:
            parcels_data.append({
                'id': parcel.id,
                'reference_cadastrale': parcel.reference_cadastrale,
                'address': parcel.address,
                'area': parcel.area,
                'zone': parcel.zone,
                'status': parcel.status,
                'owner_name': parcel.owner.full_name if parcel.owner else 'N/A',
                'created_at': parcel.created_at
            })
        
        # Export
        excel.export_parcels(parcels_data)
        
        # Stats
        stats = {
            "Total parcelles": len(parcels),
            "Superficie totale": f"{sum(p.area or 0 for p in parcels)} m²",
            "Date d'export": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        excel.add_summary_sheet(stats)
        
        return excel.build()
    
    def generate_audit_report_pdf(
        self,
        days: int = 30
    ) -> bytes:
        """
        Génère un rapport d'audit PDF complet avec statistiques détaillées
        
        Args:
            days: Nombre de jours à inclure dans le rapport
            
        Returns:
            bytes: Contenu du PDF
        """
        from backend.services.audit_service import AuditService
        
        audit_service = AuditService(self.db)
        
        # Calcul de la période
        date_from = datetime.utcnow() - timedelta(days=days)
        date_to = datetime.utcnow()
        
        # Créer le PDF
        pdf = PDFGenerator(
            title="Rapport d'Audit Complet",
            author="SIU System",
            subject=f"Rapport d'audit détaillé sur {days} jours"
        )
        
        # Métadonnées
        pdf.add_metadata_section({
            "Période d'analyse": f"Du {date_from.strftime('%d/%m/%Y')} au {date_to.strftime('%d/%m/%Y')}",
            "Durée": f"{days} jours",
            "Date de génération": datetime.now().strftime("%d/%m/%Y à %H:%M")
        })
        
        # Titre
        pdf.add_title("Rapport d'Audit Système SIU")
        pdf.add_subtitle(f"Analyse complète sur {days} jours")
        
        # Section 1: Vue d'ensemble
        pdf.add_section("1. Vue d'Ensemble")
        
        stats = audit_service.get_audit_stats(date_from=date_from, date_to=date_to)
        if stats:
            overview_data = {
                "Total des actions": stats.get('total', 0),
                "Actions réussies": stats.get('by_status', {}).get('success', 0),
                "Actions échouées": stats.get('by_status', {}).get('failure', 0),
                "Taux de réussite": f"{(stats.get('by_status', {}).get('success', 0) / stats.get('total', 1) * 100):.1f}%" if stats.get('total', 0) > 0 else "N/A"
            }
            pdf.add_key_value_table(overview_data)
        
        # Section 2: Top Utilisateurs Actifs
        pdf.add_section("2. Utilisateurs les Plus Actifs")
        
        top_users = audit_service.get_top_users(date_from=date_from, limit=10)
        if top_users:
            users_data = [["Rang", "Utilisateur", "Rôle", "Nombre d'actions"]]
            for idx, user in enumerate(top_users, 1):
                users_data.append([
                    str(idx),
                    user['username'] or f"User #{user['user_id']}",
                    user['role'] or 'N/A',
                    str(user['action_count'])
                ])
            
            pdf.add_table(users_data, header_row=True, style='striped')
        else:
            pdf.add_paragraph("Aucune activité utilisateur détectée sur la période.")
        
        # Section 3: Statistiques par Type d'Action
        pdf.add_section("3. Répartition des Actions par Type")
        
        action_stats = audit_service.get_action_statistics(date_from=date_from, date_to=date_to)
        if action_stats and action_stats.get('by_action'):
            actions_data = [["Action", "Nombre", "Pourcentage"]]
            for action in action_stats['by_action'][:15]:  # Top 15 actions
                actions_data.append([
                    action['action'],
                    str(action['count']),
                    f"{action['percentage']:.1f}%"
                ])
            
            pdf.add_table(actions_data, header_row=True, style='striped')
            
            # Total
            pdf.add_paragraph(f"<b>Total des actions analysées :</b> {action_stats['total']}")
        else:
            pdf.add_paragraph("Aucune statistique d'action disponible.")
        
        # Section 4: Actions Sensibles
        pdf.add_section("4. Actions Sensibles et Critiques")
        
        sensitive_actions = audit_service.get_sensitive_actions(date_from=date_from, limit=20)
        if sensitive_actions:
            sensitive_data = [["Date", "Action", "Utilisateur", "Entité", "Statut"]]
            for action in sensitive_actions:
                sensitive_data.append([
                    datetime.fromisoformat(action['timestamp']).strftime("%d/%m/%Y %H:%M") if isinstance(action.get('timestamp'), str) else action.get('timestamp', 'N/A'),
                    action.get('action', 'N/A'),
                    action.get('username', 'Système'),
                    f"{action.get('entity_type', 'N/A')} #{action.get('entity_id', 'N/A')}" if action.get('entity_id') else action.get('entity_type', 'N/A'),
                    action.get('status', 'N/A')
                ])
            
            pdf.add_table(sensitive_data, header_row=True, style='striped')
            pdf.add_paragraph(f"<b>Total d'actions sensibles :</b> {len(sensitive_actions)}")
        else:
            pdf.add_paragraph("✓ Aucune action sensible détectée sur la période (bon signe).")
        
        # Section 5: Analyse par Type d'Entité
        pdf.add_section("5. Activité par Type d'Entité")
        
        if stats and stats.get('by_entity'):
            entity_data = [["Type d'Entité", "Nombre d'Actions"]]
            for entity_type, count in stats['by_entity'].items():
                entity_data.append([
                    entity_type or 'Non spécifié',
                    str(count)
                ])
            
            pdf.add_table(entity_data, header_row=True, style='striped')
        else:
            pdf.add_paragraph("Aucune donnée d'entité disponible.")
        
        # Section 6: Actions Récentes (dernières 20)
        pdf.add_section("6. Historique des Actions Récentes")
        
        recent_logs = audit_service.get_audit_logs(
            date_from=date_from,
            limit=20
        )
        
        if recent_logs:
            recent_data = [["Date", "Action", "Utilisateur", "Entité", "Statut"]]
            for log in recent_logs:
                recent_data.append([
                    datetime.fromisoformat(log['timestamp']).strftime("%d/%m/%Y %H:%M") if isinstance(log.get('timestamp'), str) else str(log.get('timestamp', 'N/A')),
                    log.get('action', 'N/A'),
                    log.get('username', 'Système'),
                    f"{log.get('entity_type', '')} #{log.get('entity_id', '')}" if log.get('entity_id') else log.get('entity_type', 'N/A'),
                    log.get('status', 'success')
                ])
            
            pdf.add_table(recent_data, header_row=True, style='striped')
        else:
            pdf.add_paragraph("Aucune action récente disponible.")
        
        # Section 7: Recommandations
        pdf.add_section("7. Recommandations de Sécurité")
        
        recommendations = []
        
        # Analyser les échecs
        if stats:
            failure_count = stats.get('by_status', {}).get('failure', 0)
            total = stats.get('total', 1)
            failure_rate = (failure_count / total * 100) if total > 0 else 0
            
            if failure_rate > 5:
                recommendations.append(f"⚠️ Taux d'échec élevé ({failure_rate:.1f}%). Analyser les causes des erreurs.")
            
            if len(sensitive_actions) > 10:
                recommendations.append(f"⚠️ {len(sensitive_actions)} actions sensibles détectées. Vérifier la légitimité.")
            
            if not top_users:
                recommendations.append("ℹ️ Aucune activité utilisateur détectée. Vérifier la configuration de l'audit.")
            
            if failure_count == 0:
                recommendations.append("✓ Aucune erreur système détectée. Excellente stabilité.")
        
        if not recommendations:
            recommendations.append("✓ Le système fonctionne normalement. Aucune recommandation particulière.")
        
        for rec in recommendations:
            pdf.add_paragraph(f"• {rec}")
        
        # Pied de page
        pdf.add_paragraph("")
        pdf.add_paragraph("---")
        pdf.add_paragraph(f"<i>Rapport généré automatiquement par SIU le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>")
        
        # Générer le PDF
        return pdf.build()
    
    def export_documents_excel(
        self,
        parcel_id: Optional[str] = None
    ) -> bytes:
        """Exporte les documents vers Excel"""

        query = self.db.query(Document).filter(Document.deleted == False)

        if parcel_id:
            # Valider que l'ID est un UUID valide pour éviter les injections
            import re
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(uuid_pattern, str(parcel_id)):
                raise ValueError("ID de parcelle invalide")
            query = query.filter(Document.parcel_id == parcel_id)

        documents = query.all()

        # Créer l'Excel
        excel = ExcelService(title="Export Documents SIU")

        # Convertir
        docs_data = []
        for doc in documents:
            docs_data.append({
                'id': doc.id,
                'title': doc.title,
                'document_type': doc.document_type,
                'file_size': doc.file_size,
                'status': doc.status,
                'username': 'N/A',  # À compléter avec join
                'uploaded_at': doc.uploaded_at,
                'validated': doc.validated
            })

        excel.export_documents(docs_data)

        stats = {
            "Total documents": len(documents),
            "Taille totale": f"{sum(d.file_size or 0 for d in documents) / (1024*1024):.2f} MB",
            "Documents validés": sum(1 for d in documents if d.validated)
        }
        excel.add_summary_sheet(stats)

        return excel.build()
