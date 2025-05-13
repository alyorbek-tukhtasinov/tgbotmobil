from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import ADMIN_ID

# 1. Tugma bosilganda chiqadigan so‘rov
async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "📝 Fikringizni yozing. Taklif, shikoyat yoki savollaringizni bu yerga yuboring:"
    )

# 2. Fikrni qabul qilish va adminga yuborish
async def handle_feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.full_name
    text = update.message.text

    message = (
        f"📩 <b>Yangi fikr/taklif</b>\n"
        f"👤 <b>{username}</b> (ID: {user_id})\n\n"
        f"{text}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode='HTML')
    await update.message.reply_text("✅ Fikringiz yuborildi. Rahmat!")

# Handlerlar
feedback_button_handler = CallbackQueryHandler(ask_feedback, pattern="^feedback$")
feedback_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback_message)
