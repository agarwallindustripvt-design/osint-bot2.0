import os
import threading
from flask import Flask
import telebot

# Render Web Server Setup (24/7 Keep-Alive)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# BotFather se mila hua token yahan dalein
BOT_TOKEN = "8841976154:AAHkD3MNP9VTIQzQgYJWM3Fox1gTd9cenbg"
bot = telebot.TeleBot(BOT_TOKEN)

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = "👋 Bot start ho gaya hai!\nAap koi bhi message ya command bhejein."
    bot.reply_to(message, welcome_msg)

# /help command handler
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Kuch bhi type karke bhejie, bot aapko response dega.")

# Catch-All Handler: User koi bhi message bheje toh ye bold response aayega
@bot.message_handler(func=lambda message: True)
def echo_custom_message(message):
    # Telegram Markdown format me asterisks (*) se text bold aur bada dikhta hai
    custom_text = "*madherchod aayush*"
    bot.reply_to(message, custom_text, parse_mode="Markdown")

if __name__ == "__main__":
    # Web server ko background thread me chalayein
    t = threading.Thread(target=run_web)
    t.start()
    
    print("Bot polling start ho rahi hai...")
    bot.infinity_polling(skip_pending=True)
