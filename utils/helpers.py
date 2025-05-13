from db import get_connection

# Foydalanuvchining tanlagan tilini bazadan olish
def get_user_language(user_id: int) -> str:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT language FROM users WHERE telegram_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user['language'] if user else "uz"
    except:
        return "uz"  # Default: o'zbek

# Har bir til uchun tarjimalar
translations = {
    "welcome": {
        "uz": "Assalomu alaykum!",
        "ru": "Здравствуйте!",
        "en": "Welcome!"
    },
    "choose_category": {
        "uz": "📦 Qurilma turini tanlang:",
        "ru": "📦 Выберите категорию:",
        "en": "📦 Choose a category:"
    },
    "cart_empty": {
        "uz": "🛒 Savatchangiz bo‘sh.",
        "ru": "🛒 Ваша корзина пуста.",
        "en": "🛒 Your cart is empty."
    }
}

# Matnni tilga qarab olish
def t(key: str, lang: str) -> str:
    return translations.get(key, {}).get(lang, key)
