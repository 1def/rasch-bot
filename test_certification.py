#!/usr/bin/env python3
"""
Milliy sertifikat kabi ball berish tizimini test qilish
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.scoring import RaschAnalyzer
from app.services.pdf_generator import PDFGenerator

def test_certification_system():
    """Test ma'lumotlari bilan sertifikat tizimini sinab ko'rish"""
    
    # Test response matrix (21 talabgor, 55 savol)
    test_matrix = [
        # Talabgor 1: Ajoyib natija
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1],
        # Talabgor 2: Yaxshi natija
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,0],
        # Talabgor 3: Qoniqarli natija
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,0,0],
        # Talabgor 4: Yaxshilash kerak
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,0,0,0],
        # Talabgor 5: O'rtacha natija
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,0,0,0,0],
        # Talabgor 6-21: Turli darajadagi natijalar
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
        [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]
    ]
    
    print("🧪 Milliy sertifikat kabi ball berish tizimini test qilish...")
    
    # Rasch tahlil
    analyzer = RaschAnalyzer()
    results = analyzer.analyze_response_matrix(test_matrix)
    
    # PDF hisobot
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.generate_rasch_report(results)
    
    print(f"✅ Test muvaffaqiyatli yakunlandi!")
    print(f"📊 Natijalar: {len(results['persons'])} talabgor")
    print(f"📄 PDF hisobot: {pdf_path}")
    
    # Eng yaxshi 5 talabgor
    top_5 = sorted(results['persons'], key=lambda x: x['certification_score'], reverse=True)[:5]
    print("\n🏆 Eng yaxshi 5 talabgor:")
    for i, person in enumerate(top_5, 1):
        print(f"{i}. Talabgor {person['person_index']}: {person['certification_score']} ball ({person['certification_level']})")
    
    # Ball berish tizimi statistikasi
    excellent = sum(1 for p in results['persons'] if p['certification_score'] >= 90)
    good = sum(1 for p in results['persons'] if 75 <= p['certification_score'] < 90)
    satisfactory = sum(1 for p in results['persons'] if 60 <= p['certification_score'] < 75)
    needs_improvement = sum(1 for p in results['persons'] if p['certification_score'] < 60)
    
    print(f"\n📈 Ball berish tizimi statistikasi:")
    print(f"🏆 Ajoyib (A): {excellent} talabgor")
    print(f"🥈 Yaxshi (B): {good} talabgor")
    print(f"🥉 Qoniqarli (C): {satisfactory} talabgor")
    print(f"📚 Yaxshilash kerak (D): {needs_improvement} talabgor")

if __name__ == "__main__":
    test_certification_system()
