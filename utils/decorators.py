from db import get_connection
from config import ADMIN_ID

# Foydalanuvchini avtomatik ro‘yxatga olish
def register_user(func):
    async def wrapper(update, context):
        user = update.effective_user
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (telegram_id, fullname, language) "
                       "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE fullname=%s",
                       (user.id, user.full_name, "uz", user.full_name))
        conn.commit()
        cursor.close()
        conn.close()
        return await func(update, context)
    return wrapper

# Admin tekshiruvi
def only_admin(func):
    async def wrapper(update, context):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Sizda ruxsat yo‘q.")
            return
        return await func(update, context)
    return wrapper
