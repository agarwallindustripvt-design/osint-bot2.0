import telebot
import requests

# 1. BotFather se mila token (quotes ke andar)
BOT_TOKEN = "8841976154:AAEEOX6HPVBBzgAGuz1-DLLafety1AVkdf4"

# 2. Aapka API Configuration
API_URL = "http://agarwall.infinityfree.io/OSINT/api.php"
API_KEY = "anish-exploits"

bot = telebot.TeleBot(BOT_TOKEN)

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to OSINT Search Bot!**\n\n"
        "Aap kisi bhi number ya email ki details nikal sakte hain.\n\n"
        "📌 **Usage:** `/lookup <number/email>`\n"
        "Example: `/lookup 9876543210`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# /lookup command handler
@bot.message_handler(commands=['lookup'])
def handle_lookup(message):
    args = message.text.split()
    
    # Check karein user ne query di hai ya nahi
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Sahi Format:** `/lookup <number ya email>`\nExample: `/lookup 9876543210`", parse_mode="Markdown")
        return

    query = args[1]
    wait_msg = bot.reply_to(message, f"🔎 Searching database for: `{query}`...", parse_mode="Markdown")

    # API Request
    params = {
        "key": API_KEY,
        "query": query
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()

        if data.get("status"):
            res = data["result"]
            result_text = (
                f"✅ **RECORD FOUND**\n\n"
                f"👤 **Name:** `{res.get('name', 'N/A')}`\n"
                f"📞 **Phone:** `{res.get('phone', 'N/A')}`\n"
                f"📧 **Email:** `{res.get('email', 'N/A')}`\n"
                f"📍 **Location:** `{res.get('location', 'N/A')}`\n"
                f"📶 **Carrier:** `{res.get('carrier', 'N/A')}`\n"
                f"🌐 **IP Address:** `{res.get('ip_address', 'N/A')}`\n\n"
                f"⚡ *Powered by Anish Exploits*"
            )
        else:
            result_text = f"❌ **Error:** {data.get('message', 'No details found for this query.')}"

    except Exception as e:
        result_text = "⚠️ **Server Error:** API connection failed!"

    # Reply Message Update
    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

# Bot polling start
print("Bot started successfully...")
bot.infinity_polling()
