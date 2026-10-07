import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Render Keep-Alive Web Server
app = Flask('')

@app.route('/')
def home():
    return "OSINT Bot Active 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

BOT_TOKEN = "8841976154:AAHnnRA63w-wlexo4Iljn9h0IcsfOon2XIw"
bot = telebot.TeleBot(BOT_TOKEN)

# Interactive Menu Buttons
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🏦 IFSC LOOKUP", callback_data="ifsc_info"),
        InlineKeyboardButton("📍 PINCODE LOOKUP", callback_data="pin_info"),
        InlineKeyboardButton("🌐 IP LOOKUP", callback_data="ip_info"),
        InlineKeyboardButton("📱 PHONE LOOKUP", callback_data="num_info")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **FREE OSINT & PUBLIC LOOKUP BOT**\n\n"
        "Niche diye gaye services me se option select karein:\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    if call.data == "ifsc_info":
        bot.send_message(chat_id, "🏦 **IFSC Lookup:** Command bhejie\n`Format: /ifsc SBIN0001234`", parse_mode="Markdown")
    elif call.data == "pin_info":
        bot.send_message(chat_id, "📍 **Pincode Lookup:** Command bhejie\n`Format: /pincode 110001`", parse_mode="Markdown")
    elif call.data == "ip_info":
        bot.send_message(chat_id, "🌐 **IP Lookup:** Command bhejie\n`Format: /ip 8.8.8.8`", parse_mode="Markdown")
    elif call.data == "num_info":
        bot.send_message(chat_id, "📱 **Phone Verification:** Command bhejie\n`Format: /lookup 9876543210`", parse_mode="Markdown")

# 1. IFSC Lookup Handler
@bot.message_handler(commands=['ifsc'])
def handle_ifsc(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: `/ifsc SBIN0001234`", parse_mode="Markdown")
        return
    code = args[1].upper().strip()
    wait_msg = bot.reply_to(message, "🔎 Fetching Bank Details...")
    try:
        res = requests.get(f"https://ifsc.razorpay.com/{code}", timeout=8).json()
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
    except:
        text = "⚠️ Bank server not responding."
    bot.edit_message_text(text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# 2. Pincode Lookup Handler
@bot.message_handler(commands=['pincode'])
def handle_pincode(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: `/pincode 110001`", parse_mode="Markdown")
        return
    pin = args[1].strip()
    wait_msg = bot.reply_to(message, "🔎 Fetching Area Details...")
    try:
        res = requests.get(f"https://api.postalpincode.in/pincode/{pin}", timeout=8).json()
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

# 3. IP Lookup Handler
@bot.message_handler(commands=['ip'])
def handle_ip(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: `/ip 8.8.8.8`", parse_mode="Markdown")
        return
    ip = args[1].strip()
    wait_msg = bot.reply_to(message, "🔎 Fetching IP Details...")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        if res.get('status') == 'success':
            text = (
                f"🌐 **IP LOOKUP RESULT**\n\n"
                f"📍 **City:** `{res.get('city')}`\n"
                f"📌 **Region:** `{res.get('regionName')}`\n"
                f"🌍 **Country:** `{res.get('country')}`\n"
                f"📮 **Zip Code:** `{res.get('zip')}`\n"
                f"📡 **ISP:** `{res.get('isp')}`"
            )
        else:
            text = "❌ Invalid IP Address."
    except:
        text = "⚠️ Server error."
    bot.edit_message_text(text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# 4. Phone Verification Handler
@bot.message_handler(commands=['lookup'])
def handle_lookup(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: `/lookup 9876543210`", parse_mode="Markdown")
        return
    phone = "".join(filter(str.isdigit, args[1]))[-10:]
    wait_msg = bot.reply_to(message, f"🔎 Verifying `{phone}`...", parse_mode="Markdown")
    try:
        res = requests.get(f"https://numlookupapi.com/api/v1/validate/+91{phone}", timeout=8).json()
        carrier = res.get('carrier', 'Indian Operator')
        location = res.get('location', 'India')
    except:
        carrier = "Indian Network"
        location = "India"

    text = (
        f"📱 **PHONE RECORD**\n\n"
        f"📞 **Number:** `+91 {phone}`\n"
        f"📍 **Circle:** `{location}`\n"
        f"📶 **Carrier:** `{carrier}`"
    )
    bot.edit_message_text(text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    print("Bot starting...")
    bot.infinity_polling(skip_pending=True)
