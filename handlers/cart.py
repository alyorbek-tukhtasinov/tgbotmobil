from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from db import get_connection
from io import BytesIO
from urllib.parse import unquote_plus

# 🛒 Mahsulotni nomi orqali savatchaga qo‘shish
async def add_callback_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        user_id = query.from_user.id
        product_name = unquote_plus(query.data.replace("addcart_", ""))

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM mobiles WHERE nomi = %s", (product_name,))
        product = cursor.fetchone()

        if not product:
            await query.message.reply_text("❌ Mahsulot topilmadi.")
            return

        product_id = product['id']
        cursor.execute("INSERT INTO cart (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()

        await query.message.reply_text("✅ Mahsulot savatchaga qo‘shildi.")

    except Exception as e:
        await query.message.reply_text(f"❌ Xatolik:\n{e}")

# 👁 Savatchani ko‘rish
async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT cart.id AS cart_id, mobiles.*
        FROM cart
        JOIN mobiles ON cart.product_id = mobiles.id
        WHERE cart.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    if not items:
        if update.message:
            await update.message.reply_text("🛒 Savatchangiz bo‘sh.")
        elif update.callback_query:
            await update.callback_query.message.reply_text("🛒 Savatchangiz bo‘sh.")
        return

    for item in items:
        rasm = BytesIO(item['rasm'])
        rasm.name = "photo.jpg"
        caption = f"<b>{item['nomi']}</b>\n💰 {item['narxi']}"
        keyboard = [[InlineKeyboardButton("❌ O‘chirish", callback_data=f"remove_{item['cart_id']}")]]
        
        # ✅ Har ikki holatga javob beradi
        if update.message:
            await update.message.reply_photo(photo=rasm, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        elif update.callback_query:
            await update.callback_query.message.reply_photo(photo=rasm, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# ❌ Savatchadan mahsulotni o‘chirish
async def remove_from_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart_id = int(query.data.split("_")[1])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
    conn.commit()
    cursor.close()
    conn.close()
    await query.message.delete()

# 🔗 Handlerlar
add_button_handler = CallbackQueryHandler(add_callback_to_cart, pattern="^addcart_")
# 👇 Savatcha tugmasi uchun callback handler
cart_callback_handler = CallbackQueryHandler(view_cart, pattern="^cart$")
cart_button_handler = CommandHandler("cart", view_cart)
remove_handler = CallbackQueryHandler(remove_from_cart, pattern="^remove_")
