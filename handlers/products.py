from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_connection
from io import BytesIO
from urllib.parse import quote_plus
from handlers.menu import menu_command  # Orqaga qaytish uchun

async def product_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    kategoriya = query.data

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mobiles WHERE kategoriya = %s", (kategoriya,))
        mahsulotlar = cursor.fetchall()
        cursor.close()
        conn.close()

        if not mahsulotlar:
            await query.message.reply_text("❌ Bu bo‘limda hozircha mahsulot yo‘q.")
            return

        for item in mahsulotlar:
            rasm = BytesIO(item['rasm'])
            rasm.name = "photo.jpg"
            matn = f"<b>{item['nomi']}</b>\n💰 {item['narxi']}"

            nomi_safe = quote_plus(item['nomi'])  # Mahsulot nomini xavfsizlashtirish
            tugma = [
                [InlineKeyboardButton("🛒 Savatchaga qo‘shish", callback_data=f"addcart_{nomi_safe}")],
                [InlineKeyboardButton("🛍 Sotib olish", url=item["xarid_url"])]
            ]
            markup = InlineKeyboardMarkup(tugma)

            await query.message.reply_photo(
                photo=rasm,
                caption=matn,
                reply_markup=markup,
                parse_mode='HTML'
            )

        back_btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_menu")]
        ])
        await query.message.reply_text("⬅️ Bosh menyuga qaytish uchun:", reply_markup=back_btn)

    except Exception as e:
        await query.message.reply_text(f"❗ Xatolik yuz berdi:\n<code>{e}</code>", parse_mode='HTML')

async def go_back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await menu_command(update, context)

product_callback_handler = CallbackQueryHandler(product_callback, pattern="^(telefon|smartwatch|aksessuar|planshet)$")
back_to_menu_handler = CallbackQueryHandler(go_back_to_menu, pattern="^back_to_menu$")
