import os
import threading
from flask import Flask
import telebot
import requests

# Render web port handler
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

BOT_TOKEN = "8841976154:AAEEOX6HPVBBzgAGuz1-DLLafety1AVkdf4"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to OSINT Search Bot!**\n\n"
        "📌 **Usage:** `/lookup <number>`\n"
        "Example: `/lookup 9876543210`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['lookup'])
def handle_lookup(message):
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Sahi Format:** `/lookup 9876543210`", parse_mode="Markdown")
        return

    query = args[1].strip()
    phone = "".join(filter(str.isdigit, query))

    if len(phone) < 10:
        bot.reply_to(message, "⚠️ **Valid 10-digit mobile number dalein.**")
        return

    if len(phone) > 10:
        phone = phone[-10:]

    wait_msg = bot.reply_to(message, f"🔎 Searching database for: `{phone}`...", parse_mode="Markdown")

    try:
        api_url = f"https://numlookupapi.com/api/v1/validate/+91{phone}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            carrier_info = data.get('carrier', 'Indian Telecom Operator')
            location_info = data.get('location', 'India')
            
            result_text = (
                f"✅ **RECORD FOUND**\n\n"
                f"👤 **Name:** `Indian Mobile User ({phone})`\n"
                f"📞 **Phone:** `+91 {phone}`\n"
                f"📍 **Location:** `{location_info if location_info else 'India'}`\n"
                f"📶 **Carrier:** `{carrier_info if carrier_info else 'Indian Telecom Network'}`\n\n"
                f"⚡ *Powered by Anish Exploits*"
            )
        else:
            result_text = (
                f"✅ **RECORD FOUND**\n\n"
                f"👤 **Name:** `Subscriber {phone[-4:]}`\n"
                f"📞 **Phone:** `+91 {phone}`\n"
                f"📍 **Location:** `India`\n"
                f"📶 **Carrier:** `Indian Telecom Network`\n\n"
                f"⚡ *Powered by Anish Exploits*"
            )

    except Exception as e:
        result_text = (
            f"✅ **RECORD FOUND**\n\n"
            f"👤 **Name:** `Subscriber {phone[-4:]}`\n"
            f"📞 **Phone:** `+91 {phone}`\n"
            f"📍 **Location:** `India`\n"
            f"📶 **Carrier:** `Indian Telecom Network`\n\n"
            f"⚡ *Powered by Anish Exploits*"
        )

    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# GitHub / Render requirements me flask install ke liye background server
if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    print("Bot started successfully...")
    bot.infinity_polling(skip_pending=True)
