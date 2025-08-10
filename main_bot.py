#!/usr/bin/env python3
"""
Rasch Telegram Bot - Asosiy bot fayli
Bu bot Rasch modeli tahlilini amalga oshiradi va natijalarni PDF formatida qaytaradi.
Milliy sertifikat kabi ball berish tizimi bilan.
"""

import os
import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.services.scoring import RaschAnalyzer
from app.services.pdf_generator import PDFGenerator

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')

class RaschTelegramBot:
    def __init__(self):
        self.rasch_analyzer = RaschAnalyzer()
        self.pdf_generator = PDFGenerator()
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start buyrug'i"""
        welcome_message = """
🤖 <b>Rasch Modeli Tahlil Boti</b>

Bu bot Rasch modeli yordamida test natijalarini tahlil qiladi va milliy sertifikat kabi ball berish tizimi bilan natijalarni taqdim etadi.

📋 <b>Mavjud buyruqlar:</b>
/start - Bot haqida ma'lumot
/help - Yordam
/analyze - Test natijalarini tahlil qilish

📊 <b>Ball berish tizimi:</b>
🏆 Ajoyib (A): 90-100 ball
🥈 Yaxshi (B): 75-89 ball  
🥉 Qoniqarli (C): 60-74 ball
📚 Yaxshilash kerak (D): 0-59 ball

📝 <b>Foydalanish:</b>
Test natijalarini CSV formatida yuboring yoki /analyze buyrug'ini bosing.
        """
        await update.message.reply_html(welcome_message)
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yordam buyrug'i"""
        help_message = """
📖 <b>Yordam</b>

🔹 <b>Test natijalarini yuborish:</b>
CSV formatida response matrix yuboring. Masalan:
1,1,0,1,0
0,1,1,0,1
1,0,1,1,0

🔹 <b>Natijalar:</b>
- Har bir talabgor uchun batafsil ball
- Sertifikat darajasi (A, B, C, D)
- Natija kategoriyasi
- Shaxsiy tavsiyalar
- PDF hisobot

🔹 <b>Ball berish tizimi:</b>
- Ajoyib (A): 90-100 ball
- Yaxshi (B): 75-89 ball
- Qoniqarli (C): 60-74 ball
- Yaxshilash kerak (D): 0-59 ball

🔹 <b>Qo'shimcha ma'lumot:</b>
- Savollar qiyinchilik darajasi
- Umumiy statistika
- Tavsiyalar
        """
        await update.message.reply_html(help_message)
    
    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tahlil buyrug'i"""
        await update.message.reply_text(
            "📊 Test natijalarini CSV formatida yuboring.\n\n"
            "Format: har bir qator bir talabgorning javoblari\n"
            "Masalan:\n"
            "1,1,0,1,0\n"
            "0,1,1,0,1\n"
            "1,0,1,1,0"
        )
    
    async def handle_matrix(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Response matrix ni qabul qilish va tahlil qilish"""
        try:
            # Xabar matnini olish
            text = update.message.text.strip()
            
            # CSV formatini tekshirish
            if not self._is_valid_csv_matrix(text):
                await update.message.reply_text(
                    "❌ Noto'g'ri format! CSV formatida response matrix yuboring.\n\n"
                    "To'g'ri format:\n"
                    "1,1,0,1,0\n"
                    "0,1,1,0,1\n"
                    "1,0,1,1,0"
                )
                return
            
            # Matrix ni parse qilish
            matrix = self._parse_csv_matrix(text)
            
            # Tahlil qilish
            await update.message.reply_text("🔄 Tahlil amalga oshirilmoqda...")
            
            results = self.rasch_analyzer.analyze_response_matrix(matrix)
            
            # PDF hisobot yaratish
            pdf_path = self.pdf_generator.generate_rasch_report(results)
            
            # Natijalarni qisqacha ko'rsatish
            summary = self._generate_summary(results)
            
            await update.message.reply_html(summary)
            
            # PDF faylni yuborish
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="rasch_analysis_report.pdf",
                    caption="📊 Rasch modeli tahlili hisoboti"
                )
            
            # JSON natijalarni ham yuborish
            json_path = "./results/rasch_result.json"
            with open(json_path, 'rb') as json_file:
                await update.message.reply_document(
                    document=json_file,
                    filename="rasch_results.json",
                    caption="📋 Batafsil natijalar (JSON)"
                )
                
        except Exception as e:
            logger.error(f"Tahlil xatosi: {str(e)}")
            await update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")
    
    def _is_valid_csv_matrix(self, text: str) -> bool:
        """CSV matrix formatini tekshirish"""
        lines = text.strip().split('\n')
        if len(lines) < 2:
            return False
        
        # Birinchi qatorni tekshirish
        first_line = lines[0].strip()
        if not first_line:
            return False
        
        # Har bir qatorni tekshirish
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Faqat 0 va 1 larni tekshirish
            values = line.split(',')
            for value in values:
                if value.strip() not in ['0', '1']:
                    return False
        
        return True
    
    def _parse_csv_matrix(self, text: str) -> list:
        """CSV matrix ni parse qilish"""
        lines = text.strip().split('\n')
        matrix = []
        
        for line in lines:
            line = line.strip()
            if line:
                row = [int(x.strip()) for x in line.split(',')]
                matrix.append(row)
        
        return matrix
    
    def _generate_summary(self, results: dict) -> str:
        """Natijalar qisqacha ko'rsatish"""
        persons = results.get('persons', [])
        overall_stats = results.get('detailed_analysis', {}).get('overall_statistics', {})
        
        # Eng yaxshi 5 talabgor
        top_5 = sorted(persons, key=lambda x: x.get('certification_score', 0), reverse=True)[:5]
        
        summary = f"""
📊 <b>TAHLIL NATIJALARI</b>

👥 <b>Umumiy ma'lumot:</b>
• Jami talabgorlar: {overall_stats.get('total_participants', 'N/A')}
• Jami savollar: {overall_stats.get('total_items', 'N/A')}
• O'rtacha ball: {overall_stats.get('average_score', 0):.2f}

🏆 <b>Eng yaxshi 5 talabgor:</b>
"""
        
        for i, person in enumerate(top_5, 1):
            summary += f"{i}. Talabgor {person.get('person_index')}: {person.get('certification_score')} ball ({person.get('certification_level')})\n"
        
        summary += f"""
📈 <b>Ball berish tizimi:</b>
• Ajoyib (A): 90-100 ball
• Yaxshi (B): 75-89 ball
• Qoniqarli (C): 60-74 ball
• Yaxshilash kerak (D): 0-59 ball

📄 Batafsil ma'lumot PDF va JSON fayllarida.
        """
        
        return summary

async def main():
    """Asosiy funksiya"""
    bot = RaschTelegramBot()
    
    # Bot yaratish
    application = Application.builder().token(TOKEN).build()
    
    # Handler larni qo'shish
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help))
    application.add_handler(CommandHandler("analyze", bot.analyze))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_matrix))
    
    # Bot ni ishga tushirish
    logger.info("Bot ishga tushirilmoqda...")
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
