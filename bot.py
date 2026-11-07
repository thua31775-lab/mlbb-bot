import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# BotFather ဆီက ရထားတဲ့ Token ကို ထည့်ပါ
TOKEN = "8305016183:AAF4HMhmxP_3yMXTgVue4Zi_3knKgZVPcgo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # WebApp ဖွင့်ရန် Button ဖန်တီးခြင်း
    markup = InlineKeyboardMarkup()
    # url နေရာတွင် သင် host လုပ်ထားသော HTML WebApp ရဲ့ Link (သို့မဟုတ် local test link) ကို ထည့်ပါ
    webapp_url = "https://your-webapp-url.com" 
    markup.add(InlineKeyboardButton("🌐 Open MLBB Region Checker WebApp", web_app=telebot.types.WebAppInfo(url=webapp_url)))
    
    bot.reply_to(
        message, 
        "မင်္ဂလာပါ! MLBB User ID နဲ့ Zone ID ကို စစ်ဆေးရန် အောက်ပါ Button ကို နှိပ်ပြီး WebApp ကို အသုံးပြုပါ။", 
        reply_markup=markup
    )

# Chat ထဲတွင် စာသားဖြင့် တိုက်ရိုက် စစ်ဆေးလိုပါက (Message Handler)
@bot.message_handler(func=lambda message: True)
def check_mlbb_region(message):
    text = message.text.strip()
    
    parts = text.split()
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        bot.reply_to(message, "⚠️ ပုံစံမမှန်ပါ။ ကျေးဇူးပြု၍ `User_ID Zone_ID` ပုံစံဖြင့် ပို့ပေးပါ။ (ဥပမာ: `123456789 1234`)")
        return
    
    user_id = parts[0]
    zone_id = parts[1]
    
    sent_msg = bot.reply_to(message, "🔍 စစ်ဆေးနေပါပြီ ခဏစောင့်ပါ...")

    try:
        api_url = f"https://api.vhtext.com/mlbb?id={user_id}&zone={zone_id}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("status") == True and "result" in data:
            player_info = data.get("result", {})
            player_name = player_info.get("username", player_info.get("name", "Unknown Player"))
            server_region = player_info.get("region", "SEA / Myanmar Server")
            
            response_text = (
                f"✅ **MLBB Account Found!**\n\n"
                f"👤 **Name:** {player_name}\n"
                f"🆔 **User ID:** {user_id}\n"
                f"🌍 **Zone/Server:** {zone_id}\n"
                f"📍 **Region:** {server_region}"
            )
        else:
            response_text = (
                f"❌ **Account Not Found**\n\n"
                f"🆔 **User ID:** {user_id}\n"
                f"🌍 **Zone/Server:** {zone_id}\n\n"
                f"⚠️ ထည့်သွင်းထားသော User ID သို့မဟုတ် Zone ID မှားယွင်းနေနိုင်ပါသည်။"
            )
        
        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.edit_message_text("⚠️ API ချိတ်ဆက်ရာတွင် အမှားအယွင်း ဖြစ်သွားပါပြီ။", chat_id=message.chat.id, message_id=sent_msg.message_id)

print("Bot is running...")
bot.infinity_polling()