from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from config import ADMIN_ID

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("📱 Telefonlar", callback_data='telefon')],
        [InlineKeyboardButton("⌚ Smart soatlar", callback_data='smartwatch')],
        [InlineKeyboardButton("🎧 Aksessuarlar", callback_data='aksessuar')],
        [InlineKeyboardButton("💻 Planshetlar", callback_data='planshet')],
        [InlineKeyboardButton("🛒 Savatcha", callback_data='cart')],
        [InlineKeyboardButton("✅ Buyurtma berish", callback_data='order')],
        [InlineKeyboardButton("📝 Fikr bildirish", callback_data='feedback')],
        [InlineKeyboardButton("🌐 Tilni o‘zgartirish", callback_data='language')]
    ]

    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🛠 Admin panel", callback_data='admin')])

    markup = InlineKeyboardMarkup(keyboard)

    # ✅ Har ikkala holatni (command / callback) tekshiramiz
    if update.message:
        await update.message.reply_text("👇 Kerakli bo‘limni tanlang:", reply_markup=markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("👇 Kerakli bo‘limni tanlang:", reply_markup=markup)

menu_handler = CommandHandler("menu", menu_command)
