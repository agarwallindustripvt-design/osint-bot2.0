import telebot
import requests

BOT_TOKEN = "8841976154:AAEEOX6HPVBBzgAGuz1-DLLafety1AVkdf4"
API_URL = "http://agarwall.infinityfree.io/OSINT/api.php"
API_KEY = "anish-exploits"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to OSINT Search Bot!**\n\n"
        "📌 **Usage:** `/lookup <number/email>`\n"
        "Example: `/lookup 9876543210`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['lookup'])
def handle_lookup(message):
    args = message.text.split()
    
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **Sahi Format:** `/lookup 9876543210`", parse_mode="Markdown")
        return

    query = args[1]
    wait_msg = bot.reply_to(message, f"🔎 Searching database for: `{query}`...", parse_mode="Markdown")

    params = {
        "key": API_KEY,
        "query": query
    }

    # Custom Session to bypass security checks
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })

    try:
        response = session.get(API_URL, params=params, timeout=15)
        
        # Checking if JSON is received correctly
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
            result_text = f"❌ **Error:** {data.get('message', 'No details found.')}"

    except Exception as e:
        result_text = f"⚠️ **Server Error:** API connection failed!\n`{str(e)}`"

    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

print("Bot started...")
bot.infinity_polling()
