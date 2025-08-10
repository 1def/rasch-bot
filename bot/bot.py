from __future__ import annotations

import io
import json
import os
import tempfile
from pathlib import Path
from typing import Any, List, Optional

from dotenv import load_dotenv
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Reuse r_runner from the app package
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.core.r_runner import run_rasch_model  # type: ignore
from app.core.cleaning import clean_response_matrix  # type: ignore
from app.services.pdf_generator import create_rasch_pdf_report  # type: ignore


def read_token() -> str:
    # Load .env if present
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi. Iltimos, ENV orqali bering.")
    return token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Rasch model hisob-kitobi uchun:\n"
        "📊 CSV fayl yuboring yoki /calcjson bilan JSON matritsa yuboring\n"
        "📄 Natijalar PDF formatida qaytariladi\n"
        "- /template — namunaviy CSV faylni olish\n"
        "- /help — yordam\n"
        "Tavsiya: birinchi ustun(lar) talabgor (Ism,Fam), keyin Q1..Q40 (0/1)."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "\n".join([
            "📋 Foydalanish:",
            "📊 CSV fayl yuboring (0/1, header bo'lishi mumkin) — natija PDF qaytariladi",
            "📄 /calcjson {\"responses\": [[...],[...]]} — natija PDF",
            "📋 /template — namunaviy CSV faylni olish",
            "",
            "💡 Tavsiya: birinchi ustun(lar) talabgor (Ism,Fam), keyin Q1..Q40 (0/1)",
            "🔧 Boshqa ko'rinishlar tozalanadi, ammo xatolik ehtimoli bor",
            "",
            "📈 PDF hisobotda quyidagilar bo'ladi:",
            "• Umumiy ma'lumotlar (AIC, BIC, Log-Likelihood)",
            "• Item qiyinchilik parametrlari",
            "• Shaxs skorlari (EAP)",
            "• Vizual grafiklar"
        ])
    )


def _write_cleaned_to_csv(cleaned: List[List[Optional[int]]]) -> Path:
    tmp = tempfile.NamedTemporaryFile(prefix="rasch_clean_", suffix=".csv", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    with tmp_path.open("w", encoding="utf-8") as f:
        for row in cleaned:
            f.write(",".join("" if v is None else str(int(v)) for v in row) + "\n")
    return tmp_path


async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    doc: Document | None = update.message.document if update.message else None
    if not doc or not doc.file_name or not doc.file_name.lower().endswith(".csv"):
        return

    tf = tempfile.NamedTemporaryFile(prefix="rasch_csv_", suffix=".csv", delete=False)
    tf_path = Path(tf.name)
    tf.close()

    file = await doc.get_file()
    await file.download_to_drive(custom_path=str(tf_path))

    try:
        # Read raw CSV (simple comma split)
        rows: List[List[Any]] = []
        with tf_path.open("r", encoding="utf-8") as f:
            for line in f:
                rows.append([c for c in line.rstrip("\n").split(",")])

        cleaned = clean_response_matrix(rows)
        if not cleaned:
            await update.message.reply_text("⚠️ Jadvalni tozalash imkonsiz: savollar aniqlanmadi.")
            tf_path.unlink(missing_ok=True)
            return

        n_students = len(cleaned)
        n_questions = len(cleaned[0]) if cleaned and cleaned[0] is not None else 0
        await update.message.reply_text(f"✅ {n_students} ta talabgor, {n_questions} ta savol aniqlandi. Hisoblanmoqda...")

        tmp_path = _write_cleaned_to_csv(cleaned)
        try:
            result: dict[str, Any] = run_rasch_model(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
    except Exception as e:
        await update.message.reply_text(f"❌ Hisoblash xatosi: {e}")
        tf_path.unlink(missing_ok=True)
        return

    tf_path.unlink(missing_ok=True)

    # PDF yaratish
    try:
        pdf_content = create_rasch_pdf_report(result)
        bio = io.BytesIO(pdf_content)
        bio.name = "rasch_report.pdf"
        await update.message.reply_document(
            document=bio,
            caption=f"📊 Rasch Model Hisobot\n👥 {n_students} ta talabgor\n❓ {n_questions} ta savol"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ PDF yaratishda xato: {e}")


async def calcjson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    text = update.message.text or ""
    payload_str = text.partition(" ")[2].strip()
    if not payload_str:
        await update.message.reply_text("JSON kiritma topilmadi. Misol: /calcjson {\"responses\": [[1,0],[0,1]]}")
        return

    try:
        payload = json.loads(payload_str)
        matrix = payload.get("responses")
        cleaned = clean_response_matrix(matrix)
        if not isinstance(cleaned, list) or not cleaned:
            raise ValueError("Kiritma tozalanmadi yoki bo'sh.")
    except Exception as e:
        await update.message.reply_text(f"❌ JSON xato: {e}")
        return

    n_students = len(cleaned)
    n_questions = len(cleaned[0]) if cleaned and cleaned[0] is not None else 0
    await update.message.reply_text(f"✅ {n_students} ta talabgor, {n_questions} ta savol aniqlandi. Hisoblanmoqda...")

    with tempfile.TemporaryDirectory(prefix="rasch_") as td:
        p = Path(td) / "inp.csv"
        with p.open("w", encoding="utf-8") as f:
            for row in cleaned:
                f.write(",".join("" if v is None else str(int(v)) for v in row) + "\n")
        try:
            result = run_rasch_model(p)
        except Exception as e:
            await update.message.reply_text(f"❌ Hisoblash xatosi: {e}")
            return

    # PDF yaratish
    try:
        pdf_content = create_rasch_pdf_report(result)
        bio = io.BytesIO(pdf_content)
        bio.name = "rasch_report.pdf"
        await update.message.reply_document(
            document=bio,
            caption=f"📊 Rasch Model Hisobot\n👥 {n_students} ta talabgor\n❓ {n_questions} ta savol"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ PDF yaratishda xato: {e}")


async def template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Return sample CSV with headers and 40 items
    headers = ["Ism", "Fam"] + [f"Q{i}" for i in range(1, 41)]
    rows = [
        ["Ali", "Valiyev"] + [0, 1] * 20,
        ["Vali", "Aliyev"] + [1, 0] * 20,
        ["Malika", "Karimova"] + [1, 1, 0, 0] * 10,
    ]
    buf = io.StringIO()
    buf.write(",".join(headers) + "\n")
    for r in rows:
        buf.write(",".join(str(x) for x in r) + "\n")
    data = io.BytesIO(buf.getvalue().encode("utf-8"))
    data.name = "sample_template.csv"
    await update.message.reply_document(
        document=data,
        caption="📋 Namunaviy CSV fayl. Birinchi ustunlar talabgor ma'lumotlari, keyin savollar (0/1)"
    )


def main() -> None:
    token = read_token()
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("calcjson", calcjson))
    app.add_handler(CommandHandler("template", template))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_csv))

    print("🤖 Telegram bot ishga tushdi!")
    print(f"🔗 Token: {token[:20]}...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
