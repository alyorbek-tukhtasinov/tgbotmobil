from telegram.ext import Application
from config import BOT_TOKEN

app = Application.builder().token(BOT_TOKEN).build()

from handlers.menu import menu_handler
app.add_handler(menu_handler)

from handlers.products import product_callback_handler, back_to_menu_handler
app.add_handler(product_callback_handler)
app.add_handler(back_to_menu_handler)

from handlers.cart import cart_button_handler, remove_handler, add_button_handler, cart_callback_handler
app.add_handler(cart_button_handler)
app.add_handler(cart_callback_handler)  # 👈 SHU QATORNI QO‘SHING
app.add_handler(remove_handler)
app.add_handler(add_button_handler)

from handlers.orders import order_handler
app.add_handler(order_handler)

from handlers.feedback import feedback_button_handler, feedback_message_handler
app.add_handler(feedback_button_handler)
app.add_handler(feedback_message_handler)

from handlers.language import language_button_handler, set_language_handler
app.add_handler(language_button_handler)
app.add_handler(set_language_handler)

from handlers.admin import admin_panel_handler, admin_orders_handler, admin_stats_handler
app.add_handler(admin_panel_handler)
app.add_handler(admin_orders_handler)
app.add_handler(admin_stats_handler)

from handlers.start import start_handler
app.add_handler(start_handler)

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    app.run_polling()
