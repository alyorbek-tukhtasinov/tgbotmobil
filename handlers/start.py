from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.decorators import register_user
from utils.helpers import get_user_language, t

@register_user
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    await update.message.reply_text(
        f"{t('welcome', lang)}\n\n/menu - {t('choose_category', lang)}"
    )

start_handler = CommandHandler("start", start_command)
