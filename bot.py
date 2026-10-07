import os
import threading
from flask import Flask
import telebot

# Render Web Server Setup
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Publicly shared token replace kar diya hai security ke liye
# Telegram BotFather se new token lekar yahan paste karein
BOT_TOKEN = "8841976154:AAHkD3MNP9VTIQzQgYJWM3Fox1gTd9cenbg"
bot = telebot.TeleBot(BOT_TOKEN)

# Catch-All Handler: High-visual formatting response
@bot.message_handler(func=lambda message: True)
def send_stylish_message(message):
    # Telegram MarkdownV2 formatting for stylish / highlighted text
    stylish_text = (
        "🔴 🧡 💛 🟢 💙 💜\n"
        "✨ *MADHERCHOD AAYUSH* ✨\n"
        "🔥 `MADHERCHOD AAYUSH` 🔥\n"
        "🔴 🧡 💛 🟢 💙 💜"
    )
    bot.reply_to(message, stylish_text, parse_mode="Markdown")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    print("Bot starting...")
    bot.infinity_polling(skip_pending=True)
