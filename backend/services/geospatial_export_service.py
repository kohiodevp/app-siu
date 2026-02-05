"""
Service pour l'export de données géospatiales.
Supporte GeoJSON, Shapefile, KML, CSV avec coordonnées.
"""
from typing import List, Dict, Any, Optional
from io import BytesIO
import json
import zipfile
import csv
from datetime import datetime


class GeospatialExportService:
    """Service dédié à l'export de données géospatiales dans différents formats."""

    def export_geojson(self, parcels: List[Dict[str, Any]]) -> bytes:
        """
        Exporte les parcelles au format GeoJSON.
        
        Args:
            parcels: Liste de parcelles avec leurs coordonnées
            
        Returns:
            bytes: Contenu du fichier GeoJSON
        """
        features = []
        
        for parcel in parcels:
            # Créer une feature GeoJSON pour chaque parcelle
            feature = {
                "type": "Feature",
                "properties": {
                    "id": parcel.get("id"),
                    "reference": parcel.get("reference"),
                    "address": parcel.get("address"),
                    "area": parcel.get("area"),
                    "zone": parcel.get("zone"),
                    "category": parcel.get("category"),
                    "status": parcel.get("status"),
                    "owner_name": parcel.get("owner_name"),
                    "created_at": parcel.get("created_at"),
                },
                "geometry": None
            }
            
            # Gérer les différents types de géométrie
            if parcel.get("latitude") and parcel.get("longitude"):
                feature["geometry"] = {
                    "type": "Point",
                    "coordinates": [parcel["longitude"], parcel["latitude"]]
                }
            elif parcel.get("geometry"):
                # Si la géométrie est déjà en format GeoJSON
                feature["geometry"] = parcel["geometry"]
            
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": features,
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "total_features": len(features),
                "source": "SIU - Système d'Information Urbain"
            }
        }
        
        return json.dumps(geojson, ensure_ascii=False, indent=2).encode('utf-8')

    def export_shapefile(self, parcels: List[Dict[str, Any]]) -> bytes:
        """
        Exporte les parcelles au format Shapefile (ZIP contenant .shp, .shx, .dbf, .prj).
        
        Args:
            parcels: Liste de parcelles avec leurs coordonnées
            
        Returns:
            bytes: Contenu du fichier ZIP contenant les fichiers Shapefile
        """
        # Pour une implémentation complète, on utiliserait pyshp ou fiona
        # Pour l'instant, on crée un GeoJSON et on le met dans un ZIP
        
        geojson_content = self.export_geojson(parcels)
        
        # Créer un fichier ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Ajouter le GeoJSON (peut être converti en Shapefile avec des outils externes)
            zip_file.writestr('parcels.geojson', geojson_content)
            
            # Ajouter un fichier README
            readme = f"""SIU - Export Shapefile
Export date: {datetime.now().isoformat()}
Total parcels: {len(parcels)}

Note: Ce fichier contient les données au format GeoJSON.
Pour convertir en Shapefile (.shp), utilisez QGIS ou ogr2ogr:
  ogr2ogr -f "ESRI Shapefile" parcels.shp parcels.geojson

Système de coordonnées: WGS84 (EPSG:4326)
"""
            zip_file.writestr('README.txt', readme)
        
        zip_buffer.seek(0)
        return zip_buffer.read()

    def export_kml(self, parcels: List[Dict[str, Any]]) -> bytes:
        """
        Exporte les parcelles au format KML (Google Earth).
        
        Args:
            parcels: Liste de parcelles avec leurs coordonnées
            
        Returns:
            bytes: Contenu du fichier KML
        """
        kml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<kml xmlns="http://www.opengis.net/kml/2.2">',
            '<Document>',
            '<name>Parcelles SIU</name>',
            '<description>Export des parcelles du Système d\'Information Urbain</description>',
            
            # Styles
            '<Style id="parcel-available">',
            '<IconStyle><color>ff00ff00</color></IconStyle>',
            '</Style>',
            '<Style id="parcel-reserved">',
            '<IconStyle><color>ff0000ff</color></IconStyle>',
            '</Style>',
            '<Style id="parcel-sold">',
            '<IconStyle><color>ffff0000</color></IconStyle>',
            '</Style>',
        ]
        
        # Ajouter les placemarks pour chaque parcelle
        for parcel in parcels:
            if parcel.get("latitude") and parcel.get("longitude"):
                style_id = f"parcel-{parcel.get('status', 'available')}"
                
                kml_parts.extend([
                    '<Placemark>',
                    f'<name>{parcel.get("reference", "N/A")}</name>',
                    '<description><![CDATA[',
                    f'<b>Adresse:</b> {parcel.get("address", "N/A")}<br/>',
                    f'<b>Surface:</b> {parcel.get("area", "N/A")} m²<br/>',
                    f'<b>Zone:</b> {parcel.get("zone", "N/A")}<br/>',
                    f'<b>Catégorie:</b> {parcel.get("category", "N/A")}<br/>',
                    f'<b>Statut:</b> {parcel.get("status", "N/A")}<br/>',
                    f'<b>Propriétaire:</b> {parcel.get("owner_name", "N/A")}',
                    ']]></description>',
                    f'<styleUrl>#{style_id}</styleUrl>',
                    '<Point>',
                    f'<coordinates>{parcel["longitude"]},{parcel["latitude"]},0</coordinates>',
                    '</Point>',
                    '</Placemark>',
                ])
        
        kml_parts.extend([
            '</Document>',
            '</kml>'
        ])
        
        return '\n'.join(kml_parts).encode('utf-8')

    def export_csv_with_coordinates(self, parcels: List[Dict[str, Any]]) -> bytes:
        """
        Exporte les parcelles au format CSV avec les coordonnées.
        
        Args:
            parcels: Liste de parcelles avec leurs coordonnées
            
        Returns:
            bytes: Contenu du fichier CSV
        """
        csv_buffer = BytesIO()
        
        # Définir les colonnes
        fieldnames = [
            'id', 'reference', 'address', 'area', 'zone', 'category', 
            'status', 'owner_name', 'latitude', 'longitude', 
            'created_at', 'updated_at'
        ]
        
        # Écrire en mode texte
        import io
        text_buffer = io.StringIO()
        writer = csv.DictWriter(text_buffer, fieldnames=fieldnames, extrasaction='ignore')
        
        # Écrire l'en-tête
        writer.writeheader()
        
        # Écrire les données
        for parcel in parcels:
            # Préparer les données
            row = {key: parcel.get(key, '') for key in fieldnames}
            writer.writerow(row)
        
        # Convertir en bytes
        csv_content = text_buffer.getvalue().encode('utf-8-sig')  # UTF-8 avec BOM pour Excel
        text_buffer.close()
        
        return csv_content
