from datetime import datetime
from enum import Enum
import uuid
import hashlib
from pyproj import Transformer

class ParcelCategory(Enum):
    """Catégories possibles pour une parcelle selon les données cadastrales du Burkina Faso"""
    # Catégories originales du projet
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    MIXED_USE = "mixed-use"
    PUBLIC_SPACE = "public-space"
    
    # Catégories spécifiques au Burkina Faso
    HABITATION = "Habitation"
    CTOM = "CTOM"
    GENDARMERIE = "Gendarmerie"
    POLICE = "Police"
    CSPS = "CSPS"
    CMA = "CMA"
    CEEP = "CEEP"
    ECOLE_PRIMAIRE = "Ecole primaire"
    ECOLE_SECONDAIRE = "Ecole secondaire"
    ENSEIGNEMENT_SECONDAIRE = "Enseignement secondaire"
    COMPLEXE_SCOLAIRE = "Complexe scolaire"
    JARDIN_DENFANTS = "Jardin d'enfants"
    SANTE = "Sante"
    FORAGE = "Forage"
    FONTAINE = "Fontaine"
    CHATEAU_DEAU = "Chateau d'eau"
    MOSQUEE = "Mosquee"
    EGLISE_CATHOLIQUE = "Eglise catholique"
    CULTES = "Culte"
    CIMETIERE = "Cimetiere"
    CIMETIERE_CATHOLIQUE = "Cimetiere catholique"
    LIEU_SACRE = "Lieu sacre"
    PLACE_PUBLIQUE = "Place publique"
    JARDIN_PUBLIC = "Jardin public"
    TERRAIN_DE_SPORT = "Terrain de sport"
    PLAINE_OMNISPORTS = "Plateau omnisports"
    AIRE_DE_JEUX = "Aire de jeux"
    AIRE_DE_STATIONNEMENT = "Aire de stationnement"
    VILLAGE_TRADITIONNEL = "Village traditionnel"
    HABITAT_COLLECTIF = "Habitat collectif"
    DOMAINE_PRIVE = "Domaine prive"
    SERVITUDE_HAUTE_TENSION = "Servitude haute tension"
    CENTRE_COMMERCIAL = "Centre commercial"
    GRAND_MARCHE = "Grand marche"
    MARCHE = "Marche"
    STATION_SERVICE = "Station service"
    GARE_ROUTIERE = "Gare routiere"
    MAISON_DE_LA_FEMME = "Maison de la femme"
    MAISON_DES_JEUNES = "Maison des jeunes"
    ASSOCIATION_WOROYIRE = "Association Woroyire"
    ASSOCIATION_LOLO = "Association lolo"
    GROUPMENT_DARSALAM = "Groupement Darsalam"
    ZNA = "ZNA"
    DT = "DT"
    RA = "RA"
    RF = "RF"
    EV = "EV"
    INDEFINI = "Indefini"

    @classmethod
    def get_or_create(cls, value):
        """
        Méthode pour obtenir une catégorie existante ou créer une nouvelle catégorie dynamiquement
        
        Args:
            value: La valeur de la catégorie à chercher ou créer
            
        Returns:
            ParcelCategory: Une instance de ParcelCategory
        """
        # Essayer de trouver une catégorie existante
        for category in cls:
            if category.value == value:
                return category
        
        # Si la catégorie n'existe pas, on retourne INDEFINI comme fallback
        # Dans une implémentation complète, on pourrait ajouter dynamiquement des catégories
        return cls.INDEFINI

class DynamicParcelCategory:
    """
    Classe pour gérer les catégories de parcelles de manière dynamique
    Permet de gérer les catégories inconnues sans avoir à étendre l'énumération
    """
    
    def __init__(self, value):
        self.value = value
        self.name = self._normalize_name(value)
    
    def _normalize_name(self, value):
        """Normalise le nom de la catégorie pour les besoins d'affichage"""
        if not value:
            return "INCONNU"
        # Remplacer les caractères spéciaux et espaces par des underscores
        normalized = ''.join(c if c.isalnum() else '_' for c in value.replace(' ', '_'))
        return normalized.upper()
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"DynamicParcelCategory('{self.value}')"
    
    def __eq__(self, other):
        if isinstance(other, DynamicParcelCategory):
            return self.value == other.value
        elif isinstance(other, ParcelCategory):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False
    
    def __hash__(self):
        return hash(self.value)

def get_parcel_category(value):
    """
    Fonction utilitaire pour obtenir une catégorie de parcelle
    
    Args:
        value: La valeur de la catégorie
        
    Returns:
        ParcelCategory ou DynamicParcelCategory
    """
    if not value:
        return ParcelCategory.INDEFINI
    
    # Essayer d'abord avec l'énumération standard
    for category in ParcelCategory:
        if category.value == value:
            return category
    
    # Si non trouvé, retourner une catégorie dynamique
    return DynamicParcelCategory(value)

class Parcel:
    """
    Modèle représentant une parcelle foncière dans le système SIU

    Correspond à la FR7: Administrateurs fonciers peuvent enregistrer de nouvelles parcelles dans le système
    Correspond à la FR9: Administrateurs fonciers peuvent modifier les informations d'une parcelle existante
    Correspond à la FR34: Le système peut enregistrer l'historique complet des modifications d'une parcelle
    """

    def __init__(self, reference_cadastrale, coordinates, area, address, category=ParcelCategory.RESIDENTIAL,
                 description="", owner_id=None, cadastral_plan_ref="", created_by=None, geometry=None):
        self.id = str(uuid.uuid4())
        self.reference_cadastrale = reference_cadastrale
        self.coordinates = coordinates  # {'lat': latitude, 'lng': longitude}
        self.area = area  # en m²
        self.address = address
        self.category = category
        self.description = description
        self.geometry = geometry  # List of [lng, lat] pairs forming a polygon - optional
        self.owner_id = owner_id
        self.cadastral_plan_ref = cadastral_plan_ref
        self.created_by = created_by
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.history = []  # Historique des modifications

        # Valider les coordonnées
        self._validate_coordinates()

        # Valider la superficie
        self._validate_area()

        # Valider la géométrie si fournie (et non vide)
        if self.geometry is not None and len(self.geometry) > 0:
            self._validate_geometry()

    def _validate_coordinates(self):
        """Valide que les coordonnées sont dans les limites acceptables"""
        if not isinstance(self.coordinates, dict) or 'lat' not in self.coordinates or 'lng' not in self.coordinates:
            raise ValueError("Les coordonnées doivent être un dictionnaire avec les clés 'lat' et 'lng'")

        lat = self.coordinates['lat']
        lng = self.coordinates['lng']

        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude invalide: {lat}. Doit être entre -90 et 90")

        if not (-180 <= lng <= 180):
            raise ValueError(f"Longitude invalide: {lng}. Doit être entre -180 et 180")

    def _validate_area(self):
        """Valide que la superficie est positive"""
        if not isinstance(self.area, (int, float)) or self.area <= 0:
            raise ValueError(f"Superficie invalide: {self.area}. Doit être un nombre positif")

    def _validate_geometry(self):
        """Valide que la géométrie (polygone) est correcte"""
        if not isinstance(self.geometry, list):
            raise ValueError("La géométrie doit être une liste de coordonnées [lng, lat]")

        if len(self.geometry) < 4:
            raise ValueError("Un polygone doit avoir au moins 4 points (3 uniques + point de fermeture)")

        # Vérifier que le polygone est fermé (premier point = dernier point)
        if self.geometry[0] != self.geometry[-1]:
            raise ValueError("Le polygone doit être fermé (premier point = dernier point)")

        # Valider chaque point
        for i, point in enumerate(self.geometry):
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError(f"Point {i} invalide: doit être [lng, lat]")

            lng, lat = point
            if not isinstance(lng, (int, float)) or not isinstance(lat, (int, float)):
                raise ValueError(f"Point {i} invalide: coordonnées doivent être des nombres")

            if not (-180 <= lng <= 180):
                raise ValueError(f"Point {i} invalide: longitude {lng} hors limites [-180, 180]")

            if not (-90 <= lat <= 90):
                raise ValueError(f"Point {i} invalide: latitude {lat} hors limites [-90, 90]")

        # Vérifier que les coordonnées ne sont pas des valeurs spéciales (NaN, inf)
        for i, point in enumerate(self.geometry):
            lng, lat = point
            if lng != lng or lat != lat:  # Vérifie NaN
                raise ValueError(f"Point {i} invalide: coordonnées contiennent NaN")
            if abs(lng) == float('inf') or abs(lat) == float('inf'):  # Vérifie inf
                raise ValueError(f"Point {i} invalide: coordonnées contiennent Infinity")

    def update_info(self, **kwargs):
        """Met à jour les informations de la parcelle"""
        # Liste des champs protégés qui ne peuvent pas être modifiés
        protected_fields = {'id', 'created_at'}

        # Enregistrer l'ancienne valeur dans l'historique avant modification
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in protected_fields:
                old_value = getattr(self, key)
                if old_value != value:
                    self.history.append({
                        'field': key,
                        'old_value': old_value,
                        'new_value': value,
                        'updated_at': datetime.now(),
                        'updated_by': kwargs.get('updated_by', 'system')
                    })

                setattr(self, key, value)

        self.updated_at = datetime.now()

    def add_to_history(self, action, details, updated_by=None):
        """Ajoute une entrée à l'historique de la parcelle"""
        history_entry = {
            'action': action,
            'details': details,
            'timestamp': datetime.now(),
            'updated_by': updated_by or 'system'
        }
        self.history.append(history_entry)

    @staticmethod
    def _convert_geometry_utm_to_wgs84(geometry):
        """
        Convertit une géométrie UTM (EPSG:32630) en WGS84 (EPSG:4326)

        Args:
            geometry: Dictionnaire GeoJSON avec des coordonnées UTM

        Returns:
            Dictionnaire GeoJSON avec des coordonnées WGS84 (lat/lng)
        """
        if not geometry or not isinstance(geometry, dict):
            return geometry

        try:
            # Créer le transformer UTM -> WGS84
            transformer = Transformer.from_crs("EPSG:32630", "EPSG:4326", always_xy=True)

            geom_type = geometry.get('type')
            coords = geometry.get('coordinates', [])

            def convert_coord(coord):
                """Convertit une coordonnée [utm_x, utm_y] en [lng, lat]"""
                if isinstance(coord, (list, tuple)) and len(coord) == 2:
                    # Vérifier que les coordonnées sont valides avant conversion
                    x, y = coord
                    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                        raise ValueError(f"Coordonnées invalides: {coord}")
                    if x != x or y != y:  # Vérifie NaN
                        raise ValueError(f"Coordonnées contiennent NaN: {coord}")
                    if abs(x) == float('inf') or abs(y) == float('inf'):  # Vérifie inf
                        raise ValueError(f"Coordonnées contiennent Infinity: {coord}")

                    lng, lat = transformer.transform(x, y)
                    return [lng, lat]
                return coord

            def convert_ring(ring):
                """Convertit un anneau de polygone"""
                return [convert_coord(c) for c in ring]

            def convert_polygon(polygon):
                """Convertit un polygone (liste d'anneaux)"""
                return [convert_ring(ring) for ring in polygon]

            # Convertir selon le type de géométrie
            converted_coords = coords
            if geom_type == 'Point':
                converted_coords = convert_coord(coords)
            elif geom_type == 'Polygon':
                converted_coords = convert_polygon(coords)
            elif geom_type == 'MultiPolygon':
                converted_coords = [convert_polygon(polygon) for polygon in coords]

            return {
                'type': geom_type,
                'coordinates': converted_coords
            }
        except Exception as e:
            # Logguer l'erreur de manière plus appropriée dans un environnement de production
            # print(f"Erreur lors de la conversion de géométrie: {e}")
            # Pour l'instant, on propage l'erreur pour éviter les conversions silencieuses
            raise ValueError(f"Échec de la conversion de géométrie UTM vers WGS84: {str(e)}")

    def to_dict(self):
        """Convertit la parcelle en dictionnaire"""
        # Convertir la géométrie UTM en WGS84 si nécessaire
        geometry_wgs84 = self._convert_geometry_utm_to_wgs84(self.geometry) if self.geometry else None

        # Gérer la conversion de la catégorie pour le dictionnaire
        category_value = self.category.value if hasattr(self.category, 'value') else str(self.category)

        return {
            'id': self.id,
            'reference_cadastrale': self.reference_cadastrale,
            'coordinates': self.coordinates,
            'latitude': self.coordinates.get('lat') if isinstance(self.coordinates, dict) else None,
            'longitude': self.coordinates.get('lng') if isinstance(self.coordinates, dict) else None,
            'area': self.area,
            'address': self.address,
            'category': category_value,
            'description': self.description,
            'geometry': geometry_wgs84,
            'owner_id': self.owner_id,
            'cadastral_plan_ref': self.cadastral_plan_ref,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
            'history': self.history
        }

    @classmethod
    def _from_db_row(cls, row):
        """
        Crée une instance de Parcel depuis une ligne de base de données

        Args:
            row: sqlite3.Row object

        Returns:
            Parcel: Instance de parcelle
        """
        import json
        parcel = cls.__new__(cls)  # Créer instance sans appeler __init__
        parcel.id = row['id']
        parcel.reference_cadastrale = row['reference_cadastrale']
        parcel.coordinates = {'lat': row['coordinates_lat'], 'lng': row['coordinates_lng']}
        parcel.area = row['area']
        parcel.address = row['address']
        
        # Gérer la catégorie - priorité à la colonne 'category' si elle existe et n'est pas vide, sinon utiliser 'dest'
        category_val = row['category'] if row['category'] and row['category'].strip() else row['dest']
        
        # Utiliser la fonction utilitaire pour obtenir la catégorie
        parcel.category = get_parcel_category(category_val)
        
        parcel.description = row['description']
        parcel.geometry = json.loads(row['geometry']) if row['geometry'] else None
        parcel.owner_id = row['owner_id']
        parcel.cadastral_plan_ref = row['cadastral_plan_ref']
        parcel.created_by = row['created_by']
        parcel.created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now()
        parcel.updated_at = datetime.fromisoformat(row['updated_at']) if row['updated_at'] else datetime.now()
        parcel.history = []  # L'historique sera chargé séparément si nécessaire
        return parcel