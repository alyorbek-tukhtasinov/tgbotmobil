from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_connection
from config import ADMIN_ID

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.nomi, m.narxi FROM cart c
        JOIN mobiles m ON c.product_id = m.id
        WHERE c.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()

    if not items:
        await query.message.reply_text("❗ Savatchangiz bo‘sh, buyurtma berish uchun mahsulot tanlang.")
        return

    # 🧾 Buyurtma matni
    order_text = f"🛒 <b>Yangi buyurtma</b>\n👤 <b>{user.full_name}</b> (ID: {user_id})\n\n"
    item_list = ""
    for i, item in enumerate(items, start=1):
        item_list += f"{i}. {item['nomi']} — {item['narxi']}\n"
    order_text += item_list

    # Adminga yuborish
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=order_text,
        parse_mode='HTML'
    )

    # Bazaga saqlash (ixtiyoriy)
    cursor.execute("INSERT INTO orders (user_id, items) VALUES (%s, %s)", (user_id, item_list))
    
    # Savatchani tozalash
    cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    await query.answer("✅ Buyurtma yuborildi!")
    await query.message.reply_text("📦 Buyurtmangiz qabul qilindi. Tez orada siz bilan bog‘lanishadi.")

order_handler = CallbackQueryHandler(handle_order, pattern="^order$")
