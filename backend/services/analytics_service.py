"""
Service d'analyse et de reporting pour le système SIU
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.core.repository_interfaces import IParcelRepository, IUserRepository, IDocumentRepository, IAuditLogRepository
from backend.models.parcel import Parcel
from backend.models.user import User
from backend.models.document import Document
from backend.models.audit_log import AuditLog


class AnalyticsService:
    """
    Service pour les analyses statistiques et les rapports
    """
    
    def __init__(
        self,
        parcel_repository: IParcelRepository,
        user_repository: IUserRepository,
        document_repository: IDocumentRepository,
        audit_log_repository: IAuditLogRepository
    ):
        self.parcel_repository = parcel_repository
        self.user_repository = user_repository
        self.document_repository = document_repository
        self.audit_log_repository = audit_log_repository

    def get_dashboard_stats(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les statistiques du tableau de bord
        """
        filters = filters or {}
        
        # Calculer les statistiques de base
        total_parcels = self.parcel_repository.count(filters)
        available_parcels = self.parcel_repository.count({**filters, 'status': 'available'})
        occupied_parcels = self.parcel_repository.count({**filters, 'status': 'occupied'})
        disputed_parcels = self.parcel_repository.count({**filters, 'status': 'disputed'})
        reserved_parcels = self.parcel_repository.count({**filters, 'status': 'reserved'})
        
        # Calculer la superficie totale
        total_area = self.parcel_repository.get_total_area(filters)
        
        # Calculer la superficie moyenne
        avg_area = total_area / total_parcels if total_parcels > 0 else 0
        
        # Calculer le nombre total de propriétaires
        total_owners = self.parcel_repository.get_unique_owners_count(filters)
        
        # Calculer le nombre total de documents
        total_documents = self.document_repository.count(filters)
        
        # Calculer les activités récentes
        recent_activities = self.audit_log_repository.count({
            **filters,
            'date_from': (datetime.now() - timedelta(days=7)).isoformat()
        })
        
        # Calculer les alertes
        alerts_count = self.audit_log_repository.count({'is_alert': True, **filters})
        
        return {
            'total_parcels': total_parcels,
            'available_parcels': available_parcels,
            'occupied_parcels': occupied_parcels,
            'disputed_parcels': disputed_parcels,
            'reserved_parcels': reserved_parcels,
            'total_area': total_area,
            'average_area': avg_area,
            'total_owners': total_owners,
            'total_documents': total_documents,
            'recent_activities': recent_activities,
            'alerts_count': alerts_count
        }

    def get_parcels_by_category(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les données pour le graphique des parcelles par catégorie
        """
        filters = filters or {}
        
        # Obtenir les statistiques par catégorie
        category_stats = self.parcel_repository.get_stats_by_category(filters)
        
        labels = list(category_stats.keys())
        data = list(category_stats.values())
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Nombre de parcelles',
                'data': data,
                'backgroundColor': [
                    '#3887be', '#8a8acb', '#56b881', '#f18805', '#d22e4f', '#7f32d3',
                    '#5bb5d8', '#8fd14f', '#f55c47', '#7b68ee', '#ff69b4', '#40e0d0'
                ]
            }]
        }

    def get_parcels_by_status(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les données pour le graphique des parcelles par statut
        """
        filters = filters or {}
        
        # Obtenir les statistiques par statut
        status_stats = self.parcel_repository.get_stats_by_status(filters)
        
        labels = list(status_stats.keys())
        data = list(status_stats.values())
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Nombre de parcelles',
                'data': data,
                'backgroundColor': ['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#F44336']
            }]
        }

    def get_parcels_by_zone(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les données pour le graphique des parcelles par zone
        """
        filters = filters or {}
        
        # Obtenir les statistiques par zone
        zone_stats = self.parcel_repository.get_stats_by_zone(filters)
        
        labels = list(zone_stats.keys())
        data = list(zone_stats.values())
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Nombre de parcelles',
                'data': data,
                'backgroundColor': [
                    '#e57373', '#f06292', '#ba68c8', '#9575cd', '#7986cb',
                    '#64b5f6', '#4fc3f7', '#4dd0e1', '#4db6ac', '#81c784'
                ]
            }]
        }

    def get_area_distribution(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les données pour le graphique de distribution des surfaces
        """
        filters = filters or {}
        
        # Obtenir les statistiques de surface
        area_stats = self.parcel_repository.get_area_distribution(filters)
        
        labels = [f"{range_['min']}-{range_['max']} m²" for range_ in area_stats['ranges']]
        data = [range_['count'] for range_ in area_stats['ranges']]
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Nombre de parcelles',
                'data': data,
                'backgroundColor': '#3887be'
            }]
        }

    def get_recent_activity(self, limit: int = 20, filters: Optional[Dict[str, Any]] = None) -> list:
        """
        Récupère les activités récentes du système
        
        Args:
            limit: Nombre d'activités à retourner
            filters: Filtres optionnels
            
        Returns:
            Liste des activités récentes
        """
        try:
            from backend.database import get_db
            db = next(get_db())
            
            # Récupérer les logs d'audit récents
            query = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
            
            logs = query.all()
            
            activities = []
            for log in logs:
                activities.append({
                    'id': log.id,
                    'action': log.action,
                    'details': log.details,
                    'timestamp': log.timestamp.isoformat() if log.timestamp else None,
                    'user_id': log.user_id,
                    'parcel_id': getattr(log, 'parcel_id', None)
                })
            
            return activities
            
        except Exception as e:
            print(f"Erreur lors de la récupération des activités: {str(e)}")
            return []

    def generate_pdf_report(self, report_type: str, filters: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Génère un rapport PDF
        """
        # Pour l'instant, on simule la génération d'un rapport PDF
        # En production, on utiliserait une bibliothèque comme reportlab ou weasyprint
        import io
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Ajouter le contenu du rapport
        pdf.setTitle(f"Rapport {report_type}")
        pdf.drawString(100, height - 100, f"Rapport {report_type}")
        pdf.drawString(100, height - 120, f"Filtres appliqués: {filters}")
        pdf.drawString(100, height - 140, f"Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ajouter plus de contenu selon le type de rapport
        if report_type == 'parcels_summary':
            stats = self.get_dashboard_stats(filters)
            y_position = height - 180
            for key, value in stats.items():
                pdf.drawString(100, y_position, f"{key}: {value}")
                y_position -= 20
                if y_position < 50:  # Nouvelle page si nécessaire
                    pdf.showPage()
                    y_position = height - 100
        
        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()

    def generate_excel_report(self, report_type: str, filters: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Génère un rapport Excel
        """
        # Pour l'instant, on simule la génération d'un rapport Excel
        # En production, on utiliserait une bibliothèque comme openpyxl
        import io
        import pandas as pd
        
        # Récupérer les données selon le type de rapport
        if report_type == 'parcels_summary':
            stats = self.get_dashboard_stats(filters)
            df = pd.DataFrame([stats])
        elif report_type == 'parcels_list':
            parcels = self.parcel_repository.get_all(filters)
            df = pd.DataFrame([self._parcel_to_dict(p) for p in parcels])
        else:
            # Pour d'autres types de rapports, on peut ajouter la logique spécifique
            df = pd.DataFrame()
        
        # Créer un buffer en mémoire
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Données', index=False)
        
        buffer.seek(0)
        return buffer.getvalue()

    def generate_csv_report(self, report_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Génère un rapport CSV
        """
        import io
        import csv
        
        # Récupérer les données selon le type de rapport
        if report_type == 'parcels_summary':
            stats = self.get_dashboard_stats(filters)
            data = [stats]
        elif report_type == 'parcels_list':
            parcels = self.parcel_repository.get_all(filters)
            data = [self._parcel_to_dict(p) for p in parcels]
        else:
            data = []
        
        # Créer un buffer en mémoire
        buffer = io.StringIO()
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return buffer.getvalue()

    def get_report_history(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère l'historique des rapports générés
        """
        # Pour l'instant, on simule l'historique des rapports
        # En production, on aurait une table pour stocker les rapports générés
        reports = [
            {
                'id': f'report_{i}',
                'type': 'summary',
                'generated_at': (datetime.now() - timedelta(days=i)).isoformat(),
                'generated_by': 'admin',
                'file_size': 1024 * (i + 1)  # Taille en octets
            }
            for i in range((page - 1) * page_size, page * page_size)
        ]
        
        return {
            'items': reports,
            'total': 100,
            'page': page,
            'page_size': page_size,
            'total_pages': 10
        }

    def get_geographic_trends(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les tendances géographiques
        """
        filters = filters or {}
        
        # Obtenir les tendances géographiques
        trends = self.parcel_repository.get_geographic_trends(filters)
        
        return {
            'trends': trends,
            'period': {
                'start_date': filters.get('date_from'),
                'end_date': filters.get('date_to')
            }
        }

    def get_performance_stats(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les statistiques de performance
        """
        filters = filters or {}
        
        # Obtenir les statistiques de performance
        stats = {
            'response_times': self.audit_log_repository.get_average_response_times(filters),
            'error_rates': self.audit_log_repository.get_error_rates(filters),
            'throughput': self.audit_log_repository.get_request_throughput(filters)
        }
        
        return stats

    def get_alerts_and_anomalies(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les alertes et anomalies
        """
        filters = filters or {}
        
        # Obtenir les alertes et anomalies
        alerts = self.audit_log_repository.get_alerts(filters)
        
        return {
            'alerts': alerts,
            'count': len(alerts)
        }

    def get_predictions(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les prédictions et analyses
        """
        filters = filters or {}
        
        # Pour l'instant, on simule les prédictions
        # En production, on utiliserait des modèles ML ou des analyses statistiques
        predictions = {
            'growth_trend': 'stable',
            'demand_forecast': 'increasing',
            'risk_assessment': 'medium',
            'recommendations': ['Renforcer la surveillance', 'Améliorer les validations']
        }
        
        return predictions

    def export_raw_data(self, filters: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Exporte les données brutes
        """
        import io
        import csv
        
        # Récupérer toutes les données selon les filtres
        parcels = self.parcel_repository.get_all(filters)
        
        # Convertir en CSV
        buffer = io.StringIO()
        if parcels:
            fieldnames = self._parcel_to_dict(parcels[0]).keys()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            for parcel in parcels:
                writer.writerow(self._parcel_to_dict(parcel))
        
        # Convertir en bytes
        csv_content = buffer.getvalue()
        return csv_content.encode('utf-8')

    def get_stats_by_period(self, period: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les statistiques par période
        """
        filters = filters or {}
        
        # Obtenir les statistiques selon la période
        if period == 'daily':
            stats = self.parcel_repository.get_daily_stats(filters)
        elif period == 'weekly':
            stats = self.parcel_repository.get_weekly_stats(filters)
        elif period == 'monthly':
            stats = self.parcel_repository.get_monthly_stats(filters)
        elif period == 'quarterly':
            stats = self.parcel_repository.get_quarterly_stats(filters)
        elif period == 'yearly':
            stats = self.parcel_repository.get_yearly_stats(filters)
        else:
            stats = {}
        
        return {
            'period': period,
            'stats': stats,
            'filters': filters
        }

    def get_comparisons(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère les comparaisons
        """
        filters = filters or {}
        
        # Obtenir les comparaisons
        comparisons = self.parcel_repository.get_comparisons(filters)
        
        return {
            'comparisons': comparisons,
            'filters': filters
        }

    def get_owners_distribution(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère la distribution des propriétaires
        """
        filters = filters or {}
        
        # Obtenir la distribution des propriétaires
        distribution = self.parcel_repository.get_owners_distribution(filters)
        
        return {
            'distribution': distribution,
            'filters': filters
        }

    def get_documents_distribution(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Récupère la distribution des documents
        """
        filters = filters or {}
        
        # Obtenir la distribution des documents
        distribution = self.document_repository.get_distribution_by_type(filters)
        
        return {
            'distribution': distribution,
            'filters': filters
        }

    def get_top_zones_by_parcels(self, limit: int = 5) -> list:
        """
        Récupère les top zones par nombre de parcelles
        
        Args:
            limit: Nombre de zones à retourner
            
        Returns:
            Liste des zones avec leur nombre de parcelles
        """
        try:
            db = next(get_db())
            
            # Compter les parcelles par zone
            from sqlalchemy import func
            from backend.models.parcel import Parcel
            
            query = db.query(
                Parcel.zone,
                func.count(Parcel.id).label('parcel_count')
            ).filter(
                Parcel.zone.isnot(None),
                Parcel.zone != ''
            ).group_by(
                Parcel.zone
            ).order_by(
                func.count(Parcel.id).desc()
            ).limit(limit)
            
            results = query.all()
            
            zones = []
            for zone, count in results:
                zones.append({
                    'name': zone,
                    'parcel_count': count
                })
            
            return zones
            
        except Exception as e:
            print(f"Erreur lors de la récupération des top zones: {str(e)}")
            return []

    def _parcel_to_dict(self, parcel: Parcel) -> Dict[str, Any]:
        """
        Convertit une parcelle en dictionnaire
        """
        return {
            'id': parcel.id,
            'reference_cadastrale': getattr(parcel, 'reference_cadastrale', None),
            'coordinates_lat': getattr(parcel, 'coordinates_lat', None),
            'coordinates_lng': getattr(parcel, 'coordinates_lng', None),
            'area': getattr(parcel, 'area', None),
            'address': getattr(parcel, 'address', None),
            'category': getattr(parcel, 'category', None),
            'status': getattr(parcel, 'status', None),
            'zone': getattr(parcel, 'zone', None),
            'owner_id': getattr(parcel, 'owner_id', None),
            'created_at': getattr(parcel, 'created_at', None),
            'updated_at': getattr(parcel, 'updated_at', None)
        }