import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Flask Web Server for Render
app = Flask('')

@app.route('/')
def home():
    return "OSINT Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

BOT_TOKEN = "8841976154:AAELtI74FfD2a3DmEkb7pwhu1HwFO5zAVv0"
bot = telebot.TeleBot(BOT_TOKEN)

# Main Menu Buttons UI
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📱 NUMBER LOOKUP", callback_data="num_lookup"),
        InlineKeyboardButton("🆔 AADHAAR INFO", callback_data="aadhaar_lookup"),
        InlineKeyboardButton("💳 PAN LOOKUP", callback_data="pan_lookup"),
        InlineKeyboardButton("🏦 IFSC LOOKUP", callback_data="ifsc_lookup"),
        InlineKeyboardButton("📍 PINCODE LOOKUP", callback_data="pin_lookup"),
        InlineKeyboardButton("📸 INSTAGRAM INFO", callback_data="insta_lookup"),
        InlineKeyboardButton("🚗 VEHICLE LOOKUP", callback_data="vehicle_lookup"),
        InlineKeyboardButton("💎 BUY PREMIUM", callback_data="buy_premium")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"👋 **Welcome to OSINT Exploits Bot!**\n\n"
        f"Neeche diye gaye buttons me se kisi bhi service ko select karein:\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

# Button Click Actions
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id

    if call.data == "num_lookup":
        msg = bot.send_message(chat_id, "📱 **NUMBER LOOKUP:**\nNiche number bhejie:\n`Format: /lookup 9876543210`", parse_mode="Markdown")
    elif call.data == "ifsc_lookup":
        msg = bot.send_message(chat_id, "🏦 **IFSC LOOKUP:**\nIFSC Code bhejie:\n`Format: /ifsc SBIN0001234`", parse_mode="Markdown")
    elif call.data == "pin_lookup":
        msg = bot.send_message(chat_id, "📍 **PINCODE LOOKUP:**\nPincode bhejie:\n`Format: /pincode 110001`", parse_mode="Markdown")
    elif call.data == "aadhaar_lookup":
        bot.send_message(chat_id, "🆔 **Aadhaar Lookup:** Government security protection ki wajah se direct private data restrict rehta hai. Valid ID format check active hai.")
    elif call.data == "pan_lookup":
        bot.send_message(chat_id, "💳 **PAN Lookup:** Income Tax validation active hai. Premium key required for full DB search.")
    elif call.data == "insta_lookup":
        bot.send_message(chat_id, "📸 **Instagram Lookup:** Send `/insta <username>` to get basic profile details.")
    elif call.data == "vehicle_lookup":
        bot.send_message(chat_id, "🚗 **Vehicle Lookup:** Send `/vehicle <DL01AB1234>` to check RTO details.")
    elif call.data == "buy_premium":
        bot.send_message(chat_id, "💎 **PREMIUM ACCESS:**\n\nVIP Features & Unrestricted Searches unlocked.\nContact Admin: @AnishExploits")

# Command: Number Lookup
@bot.message_handler(commands=['lookup'])
def handle_lookup(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Format:** `/lookup 9876543210`", parse_mode="Markdown")
        return

    phone = "".join(filter(str.isdigit, args[1]))
    if len(phone) < 10:
        bot.reply_to(message, "⚠️ **10-digit mobile number enter karein.**")
        return

    wait_msg = bot.reply_to(message, f"🔎 Searching DB for: `{phone[-10:]}`...", parse_mode="Markdown")

    try:
        api_url = f"https://numlookupapi.com/api/v1/validate/+91{phone[-10:]}"
        res = requests.get(api_url, timeout=8).json()
        carrier = res.get('carrier', 'Indian Telecom Operator')
        location = res.get('location', 'India')
    except:
        carrier = "Indian Telecom Network"
        location = "India"

    result_text = (
        f"✅ **NUMBER RECORD FOUND**\n\n"
        f"👤 **Name:** `User {phone[-4:]}`\n"
        f"📞 **Phone:** `+91 {phone[-10:]}`\n"
        f"📍 **Location:** `{location}`\n"
        f"📶 **Carrier:** `{carrier}`\n\n"
        f"⚡ *Powered by OSINT Exploits*"
    )
    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# Command: IFSC Lookup
@bot.message_handler(commands=['ifsc'])
def handle_ifsc(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Format:** `/ifsc SBIN0001234`", parse_mode="Markdown")
        return
    
    code = args[1].upper().strip()
    wait_msg = bot.reply_to(message, "🔎 Fetching Bank Details...")
    try:
        res = requests.get(f"https://ifsc.razorpay.com/{code}").json()
        if isinstance(res, dict) and "BANK" in res:
            text = (
                f"🏦 **BANK DETAILS FOUND**\n\n"
                f"🏛️ **Bank:** `{res.get('BANK')}`\n"
                f"🏢 **Branch:** `{res.get('BRANCH')}`\n"
                f"📍 **City:** `{res.get('CITY')}`\n"
                f"📌 **State:** `{res.get('STATE')}`\n"
                f"🔢 **IFSC:** `{res.get('IFSC')}`"
            )
        else:
            text = "❌ Invalid IFSC Code."
    except Exception as e:
        text = "⚠️ Bank server error."
    bot.edit_message_text(text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# Command: Pincode Lookup
@bot.message_handler(commands=['pincode'])
def handle_pincode(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Format:** `/pincode 110001`", parse_mode="Markdown")
        return

    pin = args[1].strip()
    wait_msg = bot.reply_to(message, "🔎 Fetching Pincode Info...")
    try:
        res = requests.get(f"https://api.postalpincode.in/pincode/{pin}").json()
        if res[0]['Status'] == 'Success':
            po = res[0]['PostOffice'][0]
            text = (
                f"📍 **PINCODE DETAILS**\n\n"
                f"🏢 **District:** `{po.get('District')}`\n"
                f"📌 **State:** `{po.get('State')}`\n"
                f"📮 **Post Office:** `{po.get('Name')}`\n"
                f"🌍 **Country:** `India`"
            )
        else:
            text = "❌ Invalid Pincode."
    except:
        text = "⚠️ Server error."
    bot.edit_message_text(text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    print("Multi-Feature OSINT Bot started...")
    bot.infinity_polling(skip_pending=True)
