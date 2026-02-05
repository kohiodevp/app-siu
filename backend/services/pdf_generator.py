"""
Générateur PDF bas niveau avec ReportLab
Crée des PDFs professionnels avec mise en page, styles, tableaux, graphiques
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import List, Dict, Any, Optional
import io


class PDFGenerator:
    """Générateur PDF professionnel avec ReportLab"""
    
    def __init__(
        self,
        title: str = "Rapport",
        author: str = "SIU System",
        subject: str = "",
        page_size=A4
    ):
        self.title = title
        self.author = author
        self.subject = subject
        self.page_size = page_size
        self.width, self.height = page_size
        
        # Buffer pour le PDF
        self.buffer = io.BytesIO()
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Éléments du document
        self.elements = []
        
        # Configuration
        self.logo_path = None
        self.watermark_text = None
        self.footer_text = "Généré par SIU - Système d'Information Urbain"
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Style titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#673ab7'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Style sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2196f3'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Style section
        self.styles.add(ParagraphStyle(
            name='CustomSection',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#4caf50'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Style métadonnées
        self.styles.add(ParagraphStyle(
            name='Metadata',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT
        ))
    
    def add_title(self, text: str):
        """Ajoute un titre principal"""
        self.elements.append(Paragraph(text, self.styles['CustomTitle']))
        self.elements.append(Spacer(1, 12))
    
    def add_subtitle(self, text: str):
        """Ajoute un sous-titre"""
        self.elements.append(Paragraph(text, self.styles['CustomSubtitle']))
    
    def add_section(self, text: str):
        """Ajoute un titre de section"""
        self.elements.append(Paragraph(text, self.styles['CustomSection']))
    
    def add_paragraph(self, text: str, style_name: str = 'Normal'):
        """Ajoute un paragraphe"""
        style = self.styles.get(style_name, self.styles['Normal'])
        self.elements.append(Paragraph(text, style))
        self.elements.append(Spacer(1, 6))
    
    def add_table(
        self,
        data: List[List[Any]],
        col_widths: List[float] = None,
        header_row: bool = True,
        style: str = 'default'
    ):
        """
        Ajoute un tableau formaté
        
        Args:
            data: Données du tableau (liste de listes)
            col_widths: Largeurs des colonnes
            header_row: Première ligne est un en-tête
            style: Style du tableau ('default', 'striped', 'minimal')
        """
        if not data:
            return
        
        table = Table(data, colWidths=col_widths)
        
        # Styles de base
        table_style = [
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]
        
        # Style en-tête
        if header_row:
            table_style.extend([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#673ab7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ])
        
        # Styles additionnels
        if style == 'striped':
            for i in range(1, len(data)):
                if i % 2 == 0:
                    table_style.append(
                        ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f5f5'))
                    )
        
        table.setStyle(TableStyle(table_style))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))
    
    def add_key_value_table(self, data: Dict[str, Any]):
        """Ajoute un tableau clé-valeur"""
        table_data = [[k, str(v)] for k, v in data.items()]
        self.add_table(
            table_data,
            col_widths=[150, 350],
            header_row=False,
            style='minimal'
        )
    
    def add_spacer(self, height: int = 12):
        """Ajoute un espace vertical"""
        self.elements.append(Spacer(1, height))
    
    def add_page_break(self):
        """Ajoute un saut de page"""
        self.elements.append(PageBreak())
    
    def add_image(
        self,
        image_source,
        width: float = None,
        height: float = None,
        alignment: str = 'center'
    ):
        """Ajoute une image - accepte un chemin de fichier ou un objet BytesIO"""
        try:
            if isinstance(image_source, str):
                # C'est un chemin de fichier
                img = Image(image_source, width=width, height=height)
            else:
                # C'est probablement un objet BytesIO ou similaire
                # Pour les objets BytesIO, on doit les réinitialiser à 0 avant de les utiliser
                image_source.seek(0)
                img = Image(image_source, width=width, height=height)

            if alignment == 'center':
                img.hAlign = 'CENTER'
            elif alignment == 'right':
                img.hAlign = 'RIGHT'
            else:
                img.hAlign = 'LEFT'

            self.elements.append(img)
            self.elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image : {e}")
    
    def add_metadata_section(self, metadata: Dict[str, str]):
        """Ajoute une section de métadonnées"""
        metadata_text = " | ".join([f"{k}: {v}" for k, v in metadata.items()])
        self.elements.append(Paragraph(metadata_text, self.styles['Metadata']))
        self.elements.append(Spacer(1, 20))
    
    def _header_footer(self, canvas_obj, doc):
        """Callback pour en-tête et pied de page"""
        canvas_obj.saveState()
        
        # En-tête
        if self.logo_path:
            try:
                canvas_obj.drawImage(
                    self.logo_path,
                    30, self.height - 50,
                    width=50, height=50,
                    preserveAspectRatio=True
                )
            except:
                pass
        
        canvas_obj.setFont('Helvetica-Bold', 16)
        canvas_obj.setFillColor(colors.HexColor('#673ab7'))
        canvas_obj.drawString(100, self.height - 35, self.title)
        
        canvas_obj.line(30, self.height - 60, self.width - 30, self.height - 60)
        
        # Pied de page
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(colors.grey)
        
        # Texte pied de page
        canvas_obj.drawString(30, 30, self.footer_text)
        
        # Numérotation des pages
        page_num = f"Page {doc.page}"
        canvas_obj.drawRightString(self.width - 30, 30, page_num)
        
        # Date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        canvas_obj.drawCentredString(self.width / 2, 30, date_str)
        
        # Watermark optionnel
        if self.watermark_text:
            canvas_obj.setFont('Helvetica', 60)
            canvas_obj.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)
            canvas_obj.saveState()
            canvas_obj.translate(self.width / 2, self.height / 2)
            canvas_obj.rotate(45)
            canvas_obj.drawCentredString(0, 0, self.watermark_text)
            canvas_obj.restoreState()
        
        canvas_obj.restoreState()
    
    def build(self) -> bytes:
        """
        Construit le PDF et retourne les bytes
        
        Returns:
            bytes: Contenu du PDF
        """
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=self.page_size,
            rightMargin=30,
            leftMargin=30,
            topMargin=80,
            bottomMargin=50,
            title=self.title,
            author=self.author,
            subject=self.subject
        )
        
        doc.build(self.elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        self.buffer.seek(0)
        return self.buffer.getvalue()
    
    def save(self, filename: str):
        """Sauvegarde le PDF dans un fichier"""
        pdf_bytes = self.build()
        with open(filename, 'wb') as f:
            f.write(pdf_bytes)
