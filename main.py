import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "AQUI_TU_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Guardamos el último mensaje de cada usuario
user_last_message = {}

# Menú principal
def main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💳 Pagos", callback_data="pagos"))
    keyboard.add(InlineKeyboardButton("🛟 Ayuda", callback_data="ayuda"))
    return keyboard

# Menú de dispositivos
def devices_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📱 Android", callback_data="android"))
    keyboard.add(InlineKeyboardButton("🍏 iPhone", callback_data="iphone"))
    keyboard.add(InlineKeyboardButton("📺 Smart TV", callback_data="smarttv"))
    keyboard.add(InlineKeyboardButton("🔥 Fire TV Stick", callback_data="firetv"))
    keyboard.add(InlineKeyboardButton("🔙 Volver", callback_data="volver_main"))
    return keyboard

# Menú de problemas
def problems_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🛡️ VPN", callback_data="vpn"))
    keyboard.add(InlineKeyboardButton("⚫ Canales en negro", callback_data="canales"))
    keyboard.add(InlineKeyboardButton("❌ No carga la lista", callback_data="nocarga"))
    keyboard.add(InlineKeyboardButton("🔙 Volver", callback_data="volver_devices"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id,
        "👋 ¡Bienvenido al soporte de Shopremium!\n\nElige una opción:",
        reply_markup=main_menu()
    )
    user_last_message[message.from_user.id] = msg.message_id

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    # Borrar mensaje anterior
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if call.data == "pagos":
        msg = bot.send_message(chat_id, "💳 *Métodos de pago:* ...", parse_mode="Markdown")

    elif call.data == "ayuda":
        msg = bot.send_message(chat_id, "🔧 Selecciona tu dispositivo:", reply_markup=devices_menu())

    elif call.data in ["android", "iphone", "smarttv", "firetv"]:
        msg = bot.send_message(chat_id,
                               f"📌 Has elegido *{call.data.capitalize()}*.\nAhora selecciona el problema:",
                               reply_markup=problems_menu(),
                               parse_mode="Markdown")

    elif call.data in ["vpn", "canales", "nocarga"]:
        msg = bot.send_message(chat_id, f"ℹ️ Información sobre {call.data}...")

    elif call.data == "volver_main":
        msg = bot.send_message(chat_id, "🏠 Menú principal:", reply_markup=main_menu())

    elif call.data == "volver_devices":
        msg = bot.send_message(chat_id, "📱 Selecciona tu dispositivo:", reply_markup=devices_menu())

    user_last_message[user_id] = msg.message_id

bot.polling()
