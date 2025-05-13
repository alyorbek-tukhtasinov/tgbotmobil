from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_connection

# 🌐 Til tanlash tugmasi bosilganda
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("🌐 Iltimos, tilni tanlang:", reply_markup=markup)

# 🌐 Tanlangan tilni bazaga yozish
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    lang = query.data.split("_")[1]  # uz, ru, en

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id, fullname, language) VALUES (%s, %s, %s) "
                   "ON DUPLICATE KEY UPDATE language = %s",
                   (user.id, user.full_name, lang, lang))
    conn.commit()
    cursor.close()
    conn.close()

    langs = {"uz": "🇺🇿 O‘zbek", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
    await query.answer("✅ Til saqlandi")
    await query.message.reply_text(f"✅ Tanlangan til: {langs[lang]}")

language_button_handler = CallbackQueryHandler(ask_language, pattern="^language$")
set_language_handler = CallbackQueryHandler(set_language, pattern="^lang_")
