# 🤖 Rasch Telegram Bot

Bu bot Rasch modeli tahlilini amalga oshiradi va natijalarni PDF formatida qaytaradi.

## 📋 Loyiha tuzilishi

```
rasch_telegram_bot/
├── main_bot.py              # Asosiy bot fayli
├── app/                     # Ilova kodi
│   ├── main.py             # FastAPI ilovasi (keyinchalik sayt uchun)
│   ├── services/           # Xizmatlar
│   │   ├── scoring.py      # Rasch tahlil
│   │   └── pdf_generator.py # PDF yaratish
│   └── core/               # Asosiy funksiyalar
│       └── r_runner.py     # R script integratsiya
├── bot/                    # Telegram bot kodi
├── results/                # Natijalar
│   ├── rasch_result.json   # Tahlil natijalari
│   ├── rasch_report.pdf    # Hisobot fayli
│   └── README.md           # Natijalar haqida
├── tests/                  # Test fayllari
├── requirements.txt        # Python paketlar
├── .env                    # Muhit o'zgaruvchilari
└── README.md               # Bu fayl
```

## 🚀 O'rnatish

1. **Paketlarni o'rnatish:**
```bash
pip install -r requirements.txt
```

2. **Muhit o'zgaruvchilarini sozlash:**
```bash
cp .env.example .env
# .env faylida TELEGRAM_BOT_TOKEN ni o'rnating
```

3. **Botni ishga tushirish:**
```bash
python main_bot.py
```

## 📊 Foydalanish

1. Botga CSV fayl yuboring
2. Bot avtomatik tahlil qiladi
3. Natijalar PDF formatida qaytariladi

## 🔧 Xususiyatlar

- ✅ Rasch modeli tahlili
- ✅ PDF hisobot yaratish
- ✅ Grafik ko'rinishlar
- ✅ Telegram bot integratsiya
- 🔄 Web sayt integratsiya (keyinchalik)

## 📈 Natijalar

- Item qiyinchilik darajalari
- Shaxs ballari (EAP)
- Model mosligi statistikasi
- Grafik ko'rinishlar

## 🔄 Keyingi rejalar

- [ ] Web sayt integratsiya
- [ ] Ko'proq tahlil turlari
- [ ] Natijalarni saqlash
- [ ] Foydalanuvchilar paneli

## 📞 Yordam

Savollar uchun: @admin
