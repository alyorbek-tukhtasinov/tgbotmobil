from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_connection
from config import ADMIN_ID

# 🛠 Admin paneli
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    if user_id != ADMIN_ID:
        await update.callback_query.answer("❌ Sizda ruxsat yo‘q.", show_alert=True)
        return

    keyboard = [
        [InlineKeyboardButton("📦 Buyurtmalar ro‘yxati", callback_data="admin_orders")],
        [InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("🛠 Admin panel:", reply_markup=markup)

# 📦 Oxirgi buyurtmalar
async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders ORDER BY time DESC LIMIT 10")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    if not orders:
        await update.callback_query.message.reply_text("🚫 Buyurtmalar mavjud emas.")
        return

    text = "📦 <b>So‘nggi 10 ta buyurtma:</b>\n\n"
    for o in orders:
        text += f"👤 <b>{o['user_id']}</b>\n🕒 {o['time']}\n📋 {o['items']}\n\n"
    await update.callback_query.message.reply_text(text, parse_mode='HTML')

# 📊 Statistika
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM mobiles")
    products = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    text = (
        "📊 <b>Statistika:</b>\n"
        f"• Mahsulotlar: {products} ta\n"
        f"• Foydalanuvchilar: {users} ta\n"
        f"• Buyurtmalar: {orders} ta"
    )
    await update.callback_query.message.reply_text(text, parse_mode='HTML')

admin_panel_handler = CallbackQueryHandler(admin_panel, pattern="^admin$")
admin_orders_handler = CallbackQueryHandler(show_orders, pattern="^admin_orders$")
admin_stats_handler = CallbackQueryHandler(show_stats, pattern="^admin_stats$")
