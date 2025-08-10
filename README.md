# 🤖 Rasch Telegram Bot

Bu bot Rasch modeli tahlilini amalga oshiradi va milliy sertifikat kabi ball berish tizimi bilan natijalarni taqdim etadi.

## 🏆 Milliy Sertifikat Kabi Ball Berish Tizimi

### 📊 Ball Berish Standartlari:
- **🏆 Ajoyib (A)**: 90-100 ball
- **�� Yaxshi (B)**: 75-89 ball  
- **🥉 Qoniqarli (C)**: 60-74 ball
- **📚 Yaxshilash kerak (D)**: 0-59 ball

### 📋 Talabgorlar Haqida Aniqroq Ma'lumot:
- **Shaxsiy ball**: EAP (Expected A Posteriori) qiymati
- **Sertifikat darajasi**: A, B, C yoki D
- **Natija kategoriyasi**: Yuqori, O'rtacha yuqori, O'rtacha, O'rtacha past, Past
- **Batafsil tushuntirish**: Har bir talabgor uchun shaxsiy tavsiyalar
- **Standart xato**: Natija aniqligi haqida ma'lumot

## 📋 Loyiha tuzilishi

```
rasch_telegram_bot/
├── main_bot.py              # Asosiy bot fayli
├── app/                     # Ilova kodi
│   ├── main.py             # FastAPI ilovasi (keyinchalik sayt uchun)
│   ├── services/           # Xizmatlar
│   │   ├── scoring.py      # Rasch tahlil va ball berish
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
└── README.md               # Loyiha ma'lumoti
```

## 🚀 O'rnatish va ishga tushirish

### 1. Loyihani yuklab olish
```bash
git clone https://github.com/1def/rasch-bot.git
cd rasch-bot
```

### 2. Virtual environment yaratish
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 3. Paketlarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Bot tokenini sozlash
```bash
cp .env.example .env
# .env faylida TELEGRAM_BOT_TOKEN ni o'zgartiring
```

### 5. Botni ishga tushirish
```bash
python main_bot.py
```

## 📊 Foydalanish

### Telegram Bot Buyruqlari:
- `/start` - Bot haqida ma'lumot
- `/help` - Yordam
- `/analyze` - Test natijalarini tahlil qilish

### Test Natijalarini Yuborish:
CSV formatida response matrix yuboring:
```
1,1,0,1,0
0,1,1,0,1
1,0,1,1,0
```

### Natijalar:
- **PDF hisobot**: Batafsil tahlil natijalari
- **JSON fayl**: Dasturiy tahlil uchun ma'lumotlar
- **Ball berish**: Milliy sertifikat standartlari
- **Tavsiyalar**: Har bir talabgor uchun shaxsiy tavsiyalar

## �� Xususiyatlar

### 📈 Rasch Modeli Tahlili:
- Item qiyinchilik darajalari
- Shaxs ballari (EAP)
- Model mosligi statistikasi
- Standart xatolar

### 🏆 Ball Berish Tizimi:
- 100 ballik tizim
- 4 darajali sertifikat
- Shaxsiy tavsiyalar
- Natija kategoriyalari

### 📄 Hisobot Yaratish:
- PDF formatida
- O'zbekcha tushuntirishlar
- Grafik va jadvallar
- Batafsil statistika

## 🧪 Test

Test qilish uchun:
```bash
python test_certification.py
```

## 📝 Natijalar

### Talabgor Natijalari:
- **EAP ball**: Rasch modeli bo'yicha ball
- **Sertifikat ball**: 100 ballik tizimda
- **Daraja**: A, B, C yoki D
- **Kategoriya**: Natija darajasi
- **Tushuntirish**: Shaxsiy tavsiyalar

### Savol Tahlili:
- **Qiyinchilik darajasi**: Oson, O'rtacha, Qiyin, Juda qiyin
- **Tavsif**: Har bir savol haqida ma'lumot

### Umumiy Statistika:
- **Jami talabgorlar**: Test qilganlar soni
- **O'rtacha ball**: Umumiy natija
- **Eng yaxshi/yomon**: Chegaraviy natijalar
- **Tavsiyalar**: Yaxshilash uchun maslahatlar

## 🤝 Hissa qo'shish

1. Repository ni fork qiling
2. Yangi branch yarating (`git checkout -b feature/yangi-xususiyat`)
3. O'zgarishlarni commit qiling (`git commit -am 'Yangi xususiyat qo'shildi'`)
4. Branch ni push qiling (`git push origin feature/yangi-xususiyat`)
5. Pull Request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## 📞 Aloqa

Savollar va takliflar uchun:
- GitHub Issues: [https://github.com/1def/rasch-bot/issues](https://github.com/1def/rasch-bot/issues)
- Email: 1def@example.com

---

**🎯 Maqsad**: Rasch modeli yordamida aniq va adolatli ball berish tizimi yaratish
