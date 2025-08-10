import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.results_dir = "./results"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # O'zbekcha shriftlarni qo'shish
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
        except:
            pass  # Standart shriftlarni ishlatadi
    
    def generate_rasch_report(self, results: dict) -> str:
        """Rasch modeli hisobotini PDF formatida yaratadi"""
        try:
            filename = f"{self.results_dir}/rasch_report.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            
            # Stil yaratish
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='DejaVuSans-Bold' if 'DejaVuSans-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                fontName='DejaVuSans-Bold' if 'DejaVuSans-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=6,
                fontName='DejaVuSans' if 'DejaVuSans' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
            )
            
            # Sarlavha
            story.append(Paragraph("📊 RASCH MODELI TAHLILI HISOBOTI", title_style))
            story.append(Spacer(1, 20))
            
            # Vaqt
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            story.append(Paragraph(f"Hisobot vaqti: {current_time}", normal_style))
            story.append(Spacer(1, 20))
            
            # Umumiy ma'lumot
            story.append(Paragraph("📈 UMUMIY MA'LUMOT", heading_style))
            
            overall_stats = results.get('detailed_analysis', {}).get('overall_statistics', {})
            overall_data = [
                ['Parametr', 'Qiymat'],
                ['Jami ishtirokchilar', str(overall_stats.get('total_participants', 'N/A'))],
                ['Jami savollar', str(overall_stats.get('total_items', 'N/A'))],
                ['Umumiy aniqligi', f"{overall_stats.get('overall_accuracy', 0):.2f}%"],
                ['O\'rtacha ball', f"{overall_stats.get('average_score', 0):.2f}"],
                ['Eng yaxshi ball', f"{overall_stats.get('best_score', 0):.2f}"],
                ['Eng yomon ball', f"{overall_stats.get('worst_score', 0):.2f}"]
            ]
            
            overall_table = Table(overall_data, colWidths=[3*inch, 2*inch])
            overall_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(overall_table)
            story.append(Spacer(1, 20))
            
            # Sertifikat standartlari
            story.append(Paragraph("🏆 SERTIFIKAT STANDARTLARI", heading_style))
            
            cert_standards = results.get('certification_standards', {})
            cert_data = [['Daraja', 'Ball oralig\'i', 'Tavsif']]
            
            for level, info in cert_standards.items():
                level_name = {
                    'excellent': 'Ajoyib (A)',
                    'good': 'Yaxshi (B)', 
                    'satisfactory': 'Qoniqarli (C)',
                    'needs_improvement': 'Yaxshilash kerak (D)'
                }.get(level, level)
                
                cert_data.append([
                    level_name,
                    f"{info.get('min_score', 0)}-{info.get('max_score', 0)}",
                    info.get('description', '')
                ])
            
            cert_table = Table(cert_data, colWidths=[1.5*inch, 1.5*inch, 2*inch])
            cert_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(cert_table)
            story.append(PageBreak())
            
            # Talabgorlar natijalari
            story.append(Paragraph("👥 TALABGORLAR NATIJALARI", heading_style))
            
            persons = results.get('persons', [])
            if persons:
                # Eng yaxshi 10 talabgor
                story.append(Paragraph("🏅 ENG YAXSHI 10 TALABGOR", heading_style))
                
                top_persons = sorted(persons, key=lambda x: x.get('certification_score', 0), reverse=True)[:10]
                top_data = [['O\'rin', 'Talabgor', 'Ball', 'Sertifikat', 'Kategoriya']]
                
                for i, person in enumerate(top_persons, 1):
                    top_data.append([
                        str(i),
                        f"Talabgor {person.get('person_index', 'N/A')}",
                        f"{person.get('certification_score', 0)}",
                        person.get('certification_level', 'N/A'),
                        person.get('performance_category', 'N/A')
                    ])
                
                top_table = Table(top_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
                top_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(top_table)
                story.append(Spacer(1, 20))
            
            # Barcha talabgorlar
            story.append(Paragraph("📋 BARCHA TALABGORLAR RO'YXATI", heading_style))
            
            all_data = [['№', 'Talabgor', 'EAP Ball', 'Sertifikat', 'Kategoriya', 'Tushuntirish']]
            
            for person in persons:
                feedback = person.get('detailed_feedback', '')
                # Tushuntirishni qisqartirish
                if len(feedback) > 50:
                    feedback = feedback[:47] + "..."
                
                all_data.append([
                    str(person.get('person_index', 'N/A')),
                    f"Talabgor {person.get('person_index', 'N/A')}",
                    f"{person.get('eap', 0):.2f}",
                    f"{person.get('certification_score', 0)} ({person.get('certification_level', 'N/A')})",
                    person.get('performance_category', 'N/A'),
                    feedback
                ])
            
            all_table = Table(all_data, colWidths=[0.5*inch, 1*inch, 1*inch, 1.5*inch, 1*inch, 2*inch])
            all_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(all_table)
            story.append(PageBreak())
            
            # Savollar tahlili
            story.append(Paragraph("❓ SAVOLLAR TAHLILI", heading_style))
            
            items = results.get('items', [])
            if items:
                items_data = [['№', 'Savol', 'Qiyinchilik', 'Daraja', 'Tavsif']]
                
                for item in items:
                    items_data.append([
                        item.get('item_id', 'N/A'),
                        f"Savol {item.get('item_id', 'N/A').replace('Item', '')}",
                        f"{item.get('difficulty', 0):.3f}",
                        item.get('difficulty_level', 'N/A'),
                        item.get('description', '')
                    ])
                
                items_table = Table(items_data, colWidths=[0.5*inch, 1*inch, 1*inch, 1*inch, 2.5*inch])
                items_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(items_table)
                story.append(Spacer(1, 20))
            
            # Tavsiyalar
            story.append(Paragraph("💡 TAVSIYALAR", heading_style))
            
            recommendations = results.get('detailed_analysis', {}).get('recommendations', {})
            for category, recommendation in recommendations.items():
                category_name = {
                    'for_participants': 'Talabgorlar uchun:',
                    'for_test_design': 'Test dizayni uchun:',
                    'for_improvement': 'Yaxshilash uchun:'
                }.get(category, category)
                
                story.append(Paragraph(f"<b>{category_name}</b> {recommendation}", normal_style))
                story.append(Spacer(1, 10))
            
            # PDF yaratish
            doc.build(story)
            return filename
            
        except Exception as e:
            raise Exception(f"PDF yaratish xatosi: {str(e)}")
