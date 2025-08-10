#!/usr/bin/env python3
"""
Rasch Telegram Bot - Asosiy bot fayli
Bu bot Rasch modeli tahlilini amalga oshiradi va natijalarni PDF formatida qaytaradi.
"""

import os
import logging
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
🤖 Rasch Modeli Tahlil Botiga xush kelibsiz!

📊 Bu bot sizga Rasch modeli tahlilini amalga oshirishda yordam beradi.

📋 Foydalanish:
1. CSV fayl yuboring (savollar va javoblar)
2. Bot avtomatik tahlil qiladi
3. Natijalar PDF formatida qaytariladi

📈 Natijalar:
- Item qiyinchilik darajalari
- Shaxs ballari
- Model mosligi statistikasi
- Grafik ko'rinishlar

/help - Yordam olish uchun
        """
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yordam buyrug'i"""
        help_text = """
📖 Bot haqida ma'lumot:

🔹 CSV fayl formati:
- Birinchi qator: savol nomlari
- Keyingi qatorlar: har bir shaxsning javoblari
- 0 = noto'g'ri, 1 = to'g'ri

🔹 Natijalar:
- rasch_result.json: Tahlil natijalari
- rasch_report.pdf: Hisobot fayli

🔹 Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam olish
/status - Bot holati

📞 Savollar uchun: @admin
        """
        await update.message.reply_text(help_text)
    
    async def handle_csv(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """CSV faylni qayta ishlash"""
        try:
            # Faylni yuklab olish
            file = await context.bot.get_file(update.message.document.file_id)
            file_path = f"temp_{update.message.from_user.id}.csv"
            await file.download_to_drive(file_path)
            
            await update.message.reply_text("📊 Fayl yuklandi. Tahlil boshlandi...")
            
            # Rasch tahlilini amalga oshirish
            results = self.rasch_analyzer.analyze(file_path)
            
            # PDF hisobot yaratish
            pdf_path = self.pdf_generator.generate_report(results, f"report_{update.message.from_user.id}.pdf")
            
            # Natijalarni yuborish
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    caption="📈 Rasch modeli tahlil natijalari"
                )
            
            # Vaqtinchalik fayllarni o'chirish
            os.remove(file_path)
            os.remove(pdf_path)
            
        except Exception as e:
            logger.error(f"Xatolik: {e}")
            await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot holati"""
        status_text = """
🟢 Bot faol holatda

📊 Tahlil qilingan fayllar: 0
📈 Natijalar: Tayyor
🔧 Tizim: Ishga tushgan

✅ Barcha funksiyalar ishlayapti
        """
        await update.message.reply_text(status_text)

def main():
    """Asosiy funksiya"""
    bot = RaschTelegramBot()
    
    # Bot ilovasini yaratish
    application = Application.builder().token(TOKEN).build()
    
    # Buyruqlarni qo'shish
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("status", bot.status))
    
    # CSV fayllarni qayta ishlash
    application.add_handler(MessageHandler(filters.Document.ALL, bot.handle_csv))
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    application.run_polling()

if __name__ == '__main__':
    main()
