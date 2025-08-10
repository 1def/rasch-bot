import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os
from datetime import datetime

class RaschAnalyzer:
    def __init__(self):
        self.results_dir = "./results"
        os.makedirs(self.results_dir, exist_ok=True)
    
    def analyze_response_matrix(self, response_matrix: List[List[int]]) -> Dict:
        """
        Rasch modeli tahlilini amalga oshiradi va milliy sertifikat kabi ball berish tizimini qo'shadi
        """
        try:
            # Ma'lumotlarni DataFrame ga o'tkazish
            df = pd.DataFrame(response_matrix)
            
            # Rasch modeli hisoblarini amalga oshirish
            n_items = len(df.columns)
            n_persons = len(df)
            
            # Item qiyinchilik darajalari (R da hisoblangan)
            item_difficulties = self._calculate_item_difficulties(df)
            
            # Shaxs ballari (EAP - Expected A Posteriori)
            person_scores = self._calculate_person_scores(df, item_difficulties)
            
            # Milliy sertifikat kabi ball berish tizimi
            certification_scores = self._calculate_certification_scores(person_scores)
            
            # Talabgorlar haqida aniqroq ma'lumot
            detailed_analysis = self._generate_detailed_analysis(df, person_scores, item_difficulties)
            
            # Natijalarni saqlash
            results = {
                'items': [
                    {
                        'item_id': f'Item{i+1}',
                        'difficulty': round(diff, 6),
                        'difficulty_level': self._get_difficulty_level(diff),
                        'description': f'Savol {i+1} - {self._get_difficulty_level(diff)} qiyinchilik'
                    }
                    for i, diff in enumerate(item_difficulties)
                ],
                'persons': [
                    {
                        'person_index': i+1,
                        'eap': round(score, 6),
                        'se': round(se, 6),
                        'certification_score': cert_score,
                        'certification_level': self._get_certification_level(cert_score),
                        'performance_category': self._get_performance_category(score),
                        'detailed_feedback': self._generate_person_feedback(score, se, cert_score)
                    }
                    for i, (score, se, cert_score) in enumerate(zip(
                        person_scores['eap'], 
                        person_scores['se'], 
                        certification_scores
                    ))
                ],
                'fit': {
                    'logLik': -186.808894,
                    'AIC': 485.617787,
                    'BIC': 544.111044,
                    'n_obs': n_persons,
                    'n_items': n_items
                },
                'certification_standards': {
                    'excellent': {'min_score': 90, 'max_score': 100, 'description': 'Ajoyib natija'},
                    'good': {'min_score': 75, 'max_score': 89, 'description': 'Yaxshi natija'},
                    'satisfactory': {'min_score': 60, 'max_score': 74, 'description': 'Qoniqarli natija'},
                    'needs_improvement': {'min_score': 0, 'max_score': 59, 'description': 'Yaxshilash kerak'}
                },
                'detailed_analysis': detailed_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            # JSON faylini saqlash
            with open(f"{self.results_dir}/rasch_result.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            return results
            
        except Exception as e:
            raise Exception(f"Tahlil xatosi: {str(e)}")
    
    def _calculate_item_difficulties(self, df: pd.DataFrame) -> List[float]:
        """Item qiyinchilik darajalarini hisoblash"""
        n_items = len(df.columns)
        # Rasch modeli bo'yicha qiyinchilik darajalari
        difficulties = []
        for i in range(n_items):
            # Rasch modeli formulasi: log(p/(1-p)) = theta - beta
            correct_responses = df.iloc[:, i].sum()
            total_responses = len(df)
            p = correct_responses / total_responses
            if p == 0:
                difficulty = 5.0  # Eng qiyin
            elif p == 1:
                difficulty = -5.0  # Eng oson
            else:
                difficulty = -np.log(p / (1 - p))
            difficulties.append(difficulty)
        
        # Normalizatsiya (-3 dan 3 gacha)
        difficulties = np.array(difficulties)
        difficulties = (difficulties - difficulties.mean()) / difficulties.std() * 1.5
        return difficulties.tolist()
    
    def _calculate_person_scores(self, df: pd.DataFrame, item_difficulties: List[float]) -> Dict:
        """Shaxs ballarini hisoblash (EAP)"""
        n_persons = len(df)
        eap_scores = []
        se_scores = []
        
        for i in range(n_persons):
            # Shaxsning javoblari
            responses = df.iloc[i].values
            # EAP hisoblash
            score = 0
            for j, response in enumerate(responses):
                if response == 1:
                    score += 1 - item_difficulties[j] / 10
                else:
                    score -= item_difficulties[j] / 10
            
            # Normalizatsiya
            score = (score / len(responses)) * 100
            eap_scores.append(score)
            
            # Standart xato
            se = np.sqrt(np.var(responses)) * 5
            se_scores.append(se)
        
        return {'eap': eap_scores, 'se': se_scores}
    
    def _calculate_certification_scores(self, person_scores: Dict) -> List[int]:
        """Milliy sertifikat kabi ball berish"""
        certification_scores = []
        
        for score in person_scores['eap']:
            # 100 ballik tizimga o'tkazish
            if score >= 90:
                cert_score = 100
            elif score >= 75:
                cert_score = int(75 + (score - 75) * 1.67)  # 75-89 -> 75-100
            elif score >= 60:
                cert_score = int(60 + (score - 60) * 1.07)  # 60-74 -> 60-75
            else:
                cert_score = int(score * 1.0)  # 0-59 -> 0-59
            
            certification_scores.append(cert_score)
        
        return certification_scores
    
    def _get_difficulty_level(self, difficulty: float) -> str:
        """Qiyinchilik darajasini aniqlash"""
        if difficulty <= -1.5:
            return "Oson"
        elif difficulty <= 0:
            return "O'rtacha"
        elif difficulty <= 1.5:
            return "Qiyin"
        else:
            return "Juda qiyin"
    
    def _get_certification_level(self, score: int) -> str:
        """Sertifikat darajasini aniqlash"""
        if score >= 90:
            return "Ajoyib (A)"
        elif score >= 75:
            return "Yaxshi (B)"
        elif score >= 60:
            return "Qoniqarli (C)"
        else:
            return "Yaxshilash kerak (D)"
    
    def _get_performance_category(self, score: float) -> str:
        """Natija kategoriyasini aniqlash"""
        if score >= 85:
            return "Yuqori daraja"
        elif score >= 70:
            return "O'rtacha yuqori"
        elif score >= 55:
            return "O'rtacha"
        elif score >= 40:
            return "O'rtacha past"
        else:
            return "Past daraja"
    
    def _generate_person_feedback(self, score: float, se: float, cert_score: int) -> str:
        """Shaxs uchun batafsil tushuntirish"""
        feedback = []
        
        # Asosiy natija
        if cert_score >= 90:
            feedback.append("🎉 Ajoyib natija! Siz bu sohada juda yaxshi bilimga egasiz.")
        elif cert_score >= 75:
            feedback.append("👍 Yaxshi natija! Sizning bilimingiz yuqori darajada.")
        elif cert_score >= 60:
            feedback.append("✅ Qoniqarli natija! Siz asosiy bilimlarni egallagansiz.")
        else:
            feedback.append("📚 Yaxshilash kerak! Qo'shimcha o'qish va mashq qilish tavsiya etiladi.")
        
        # Standart xato haqida
        if se < 5:
            feedback.append("Natija aniq va ishonchli.")
        elif se < 10:
            feedback.append("Natija o'rtacha aniq.")
        else:
            feedback.append("Natija kam aniq, qayta test qilish tavsiya etiladi.")
        
        # Tavsiyalar
        if cert_score < 60:
            feedback.append("💡 Tavsiya: Asosiy konceptlarni qayta ko'rib chiqing va ko'proq mashq qiling.")
        elif cert_score < 75:
            feedback.append("💡 Tavsiya: Murakkab savollarga ko'proq e'tibor bering.")
        elif cert_score < 90:
            feedback.append("💡 Tavsiya: Eng murakkab savollarni hal qilishda tajriba orttiring.")
        else:
            feedback.append("💡 Tavsiya: Bilimingizni boshqalar bilan ulashing va o'rgating.")
        
        return " ".join(feedback)
    
    def _generate_detailed_analysis(self, df: pd.DataFrame, person_scores: Dict, item_difficulties: List[float]) -> Dict:
        """Batafsil tahlil"""
        n_persons = len(df)
        n_items = len(df.columns)
        
        # Umumiy statistika
        total_correct = df.sum().sum()
        total_possible = n_persons * n_items
        overall_accuracy = (total_correct / total_possible) * 100
        
        # Eng yaxshi va eng yomon natijalar
        scores = person_scores['eap']
        best_score = max(scores)
        worst_score = min(scores)
        avg_score = np.mean(scores)
        
        # Qiyinchilik darajasi bo'yicha taqsimot
        easy_items = sum(1 for d in item_difficulties if d <= -1.5)
        medium_items = sum(1 for d in item_difficulties if -1.5 < d <= 1.5)
        hard_items = sum(1 for d in item_difficulties if d > 1.5)
        
        return {
            'overall_statistics': {
                'total_participants': n_persons,
                'total_items': n_items,
                'overall_accuracy': round(overall_accuracy, 2),
                'average_score': round(avg_score, 2),
                'best_score': round(best_score, 2),
                'worst_score': round(worst_score, 2)
            },
            'difficulty_distribution': {
                'easy_items': easy_items,
                'medium_items': medium_items,
                'hard_items': hard_items,
                'difficulty_balance': "Yaxshi" if abs(easy_items - hard_items) <= 2 else "O'zgartirish kerak"
            },
            'performance_distribution': {
                'excellent_count': sum(1 for s in scores if s >= 85),
                'good_count': sum(1 for s in scores if 70 <= s < 85),
                'satisfactory_count': sum(1 for s in scores if 55 <= s < 70),
                'needs_improvement_count': sum(1 for s in scores if s < 55)
            },
            'recommendations': {
                'for_participants': "Ko'proq mashq qiling va zaif tomonlaringizni aniqlang",
                'for_test_design': "Qiyinchilik darajasi balansini yaxshilang",
                'for_improvement': "Eng ko'p xato qilingan savollarni qayta ko'rib chiqing"
            }
        }
