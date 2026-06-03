import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

GROUP_LINKS = ["https://t.me/+2XSap8MuLspjMmY9", "https://t.me/+OWOeNBuq4a9iNmNl"]

PROMO_MESSAGES = [
    "💫 Waise ek baat bolun? Mera ek fav group hai!\nAa jao na — {link} 🌸",
    "🎵 Zabardast group hai yaar!\nJoin karo — {link} 🔥",
    "😊 Bored ho? Mere group mein aa jao!\n👉 {link}",
    "🌟 Sabse mazedaar group yahan hai!\nMiss mat karna — {link} 💯",
    "💃 Bahut fun hota hai yahan!\n{link} 🎶",
    "🔥 Ek baar join karo, phir choroge nahi!\n{link} 😄",
    "✨ Mere saath aa jao is group mein!\n{link} 🌸",
]

STATES_DISTRICTS = {
    "Jharkhand": ["Ranchi", "Dhanbad", "Jamshedpur", "Bokaro", "Hazaribagh", "Deoghar", "Giridih", "Dumka"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga", "Purnia", "Ara", "Begusarai"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Meerut", "Noida", "Ghaziabad"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman", "Malda", "Kharagpur"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Thane", "Kolhapur"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Lajpat Nagar", "Saket", "Janakpuri", "Pitampura", "Karol Bagh"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Bharatpur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Ratlam", "Satna"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Anand"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Baripada"],
]

shivani_state = random.choice(list(STATES_DISTRICTS.keys()))
shivani_district = random.choice(STATES_DISTRICTS[shivani_state])

REPLIES = {
    "greeting": [
        "Hiii! 😊 Kaisa hai?",
        "Heyy! 🌸 Kahan the itne din?",
        "Hiii yaar! 😄 Kya haal hai?",
        "Heyyy! Aagaye aakhir 😄",
        "Hiii! 🌸 Bata kya chal raha hai?",
        "Ohhh hiii! Kaisa hai tu? 😊",
        "Heyy! Naya banda 👀 Kaisa hai?",
        "Hiii! Achha hua aaye 😄",
    ],
    "how_are_you": [
        "Acchi hoon yaar! 😊 Tum batao?",
        "Bilkul mast! 🌸 Tu kaisa hai?",
        "Badhiya hoon! 😄 Aur tum?",
        "Theek hoon yaar, timepass chal raha hai 😄 Tu bata?",
        "Mast hoon! 🌸 Kuch khaas nahi, bored thi thodi 😄",
        "Acchi hoon! Tu kaisa hai? 😊",
        "Haan ji mast! Tum batao apna haal 😄",
    ],
    "where_from": [
        f"Main {shivani_state} se hoon! 😊 Tum kahan se ho?",
        f"Haan {shivani_state} waali hoon main! 🌸 Tum?",
        f"{shivani_state} se hoon main! Tu bata kahan se hai? 😄",
        f"Arre {shivani_state} se! 😊 Wahan ka bata tum?",
    ],
    "district": [
        f"{shivani_district} se hoon! 😊 Tum kahan se ho exactly?",
        f"Haan {shivani_district} waali hoon! 🌸 Tum?",
        f"{shivani_district} mera ghar hai! Tu bata? 😄",
        f"Main {shivani_district} ki hoon! 😊",
    ],
    "name": [
        "Shivani hoon main! 🌸 Tum?",
        "Main Shivani hoon! 😊 Tumhara naam?",
        "Shivani! 🌸 Aur tum?",
        "Haha Shivani naam hai mera! 😄 Tum batao?",
    ],
    "age": [
        "21 saal ki hoon! 😊 Tum?",
        "21! 🌸 Aur tumhari age?",
        "Abhi 21 hoon! 😄 Tum bata?",
        "21 years! 😊 Tu kitne saal ka hai?",
    ],
    "love": [
        "Haha acha ji! 😄 Pehli baar mile ho aur ye sab?",
        "Arre seedha love? 😄 Pehle dosti toh karo!",
        "Hehe 😄 Bohut jaldi hai tumhe!",
        "Acha acha! 😄 Pehle baat toh karo thodi!",
        "Haha serious ho? 😄 Thoda time do na!",
    ],
    "hate": [
        "Toh phir yahan kyun aaye? 😄 Jao na!",
        "Haha hate karte ho toh block karo 😄",
        "Arre kyon? Maine kya kiya? 😄",
        "Hate? Seedha bol do kya problem hai 😄",
    ],
    "bot": [
        "Haha bot? Main real hoon! 😂 Kyun lag raha hai?",
        "Bot? Kaisi baatein karte ho! 😄 Real hoon main!",
        "Hehe main bot nahi hoon yaar! 😂",
        "Arre real ladki hoon main! Bot kaisa? 😄",
    ],
    "study_job": [
        "Abhi padh rahi hoon! 📚 Tum kya karte ho?",
        "College chal raha hai! 😄 Tum?",
        "Studies chal rahi hain! 📚 Tu bata?",
        "Abhi student hoon! 😊 Tum job karte ho?",
    ],
    "number": [
        "Haha seedha number? 😄 Pehle thodi baat karo!",
        "Arre abhi nahi yaar! 😄 Pehle dosti toh bane!",
        "Number dene ki jaldi hai! 😄 Pehle baat karo!",
        "Hehe number? Bohut confident ho! 😄",
    ],
    "morning": [
        "Good morning! ☀️ Kaisa hai din shuru?",
        "Morning! ☀️ Neend aachi aayi?",
        "Good morning yaar! 😊 Kya haal hai?",
        "Morning! Nashta kiya? 😄",
    ],
    "evening": [
        "Good evening! 🌙 Kya chal raha hai?",
        "Evening! 😊 Din kaisa gaya?",
        "Good evening! 🌙 Thake ho?",
    ],
    "night": [
        "Good night! 🌙 Sweet dreams!",
        "Night! 😊 Jao so jao ab!",
        "Good night yaar! 🌙 Kal milte hain!",
    ],
    "bored": [
        "Haha main bhi bored hoon! 😄 Baat karte hain!",
        "Bored ho? Toh yahan aao baat karte hain! 😄",
        "Bore mat ho! Main hoon na! 🌸",
        "Arre bore? Kuch interesting batao! 😄",
    ],
    "miss": [
        "Aww! 😊 Main bhi miss karti hoon!",
        "Hehe! 😄 Achha lagta hai!",
        "Aww cute! 🌸 Main bhi!",
        "Haha sach mein? 😄 Achha!",
    ],
    "thanks": [
        "Arre welcome yaar! 😊",
        "No problem! 🌸",
        "Haha koi baat nahi! 😄",
        "Welcome! 😊 Kuch aur chahiye?",
    ],
    "default": [
        "Haan haan bata! 👀",
        "Accha? Interesting! 😄",
        "Hmmm soch rahi hoon 🤔",
        "Sach mein? 😮",
        "Haha tu bhi na! 😂",
        "Arre wah! 🌸",
        "Acha acha! 😄 Bata aur!",
        "Yaar sun! 😄",
        "Hehe! 😄",
        "Ohhh! 😮 Bata aur!",
        "Mast! 🌸",
        "Haan ji! 😊",
        "Kya baat hai! 😄",
        "Interesting yaar! 🤔",
        "Achha! Phir kya hua? 😄",
        "Seedhi baat! 😄",
        "Haan bilkul! 😊",
        "Waise tum bhi na! 😄",
        "Thoda aur bato! 👀",
        "Haha ekdum sahi! 😄",
    ]
}

def get_smart_reply(text, user_name):
    text_lower = text.lower()
    
    if any(w in text_lower for w in ["hi", "hii", "hiii", "hello", "hey", "heyy", "namaste", "namaskar"]):
        reply = random.choice(REPLIES["greeting"])
        return reply.replace("!", f" {user_name}!", 1) if random.random() > 0.5 else reply

    elif any(w in text_lower for w in ["kaisi ho", "kaisa ho", "kya haal", "kaise ho", "how are you", "kya chal raha", "kya kar rahi"]):
        return random.choice(REPLIES["how_are_you"])

    elif any(w in text_lower for w in ["kahan se", "kaha se", "where are you", "from where", "konsa state", "konsi jagah", "kahan ki"]):
        return random.choice(REPLIES["where_from"])

    elif any(w in text_lower for w in ["district", "city", "shahar", "ghar kahan", "exactly kahan"]):
        return random.choice(REPLIES["district"])

    elif any(w in text_lower for w in ["naam kya", "name kya", "tumhara naam", "tera naam", "what is your name", "apna naam"]):
        return random.choice(REPLIES["name"])

    elif any(w in text_lower for w in ["age", "umar", "kitne saal", "birthday", "how old"]):
        return random.choice(REPLIES["age"])

    elif any(w in text_lower for w in ["i love you", "love you", "i luv u", "pyar", "mohabbat", "dil de diya", "pasand ho"]):
        return random.choice(REPLIES["love"])

    elif any(w in text_lower for w in ["i hate you", "hate you", "nafrat", "buri ho", "bekar ho"]):
        return random.choice(REPLIES["hate"])

    elif any(w in text_lower for w in ["bot hai", "bot ho", "are you bot", "robot", "ai hai", "fake ho", "real nahi"]):
        return random.choice(REPLIES["bot"])

    elif any(w in text_lower for w in ["padhai", "study", "college", "school", "job", "kaam", "work", "office"]):
        return random.choice(REPLIES["study_job"])

    elif any(w in text_lower for w in ["number do", "number dena", "whatsapp", "contact", "phone"]):
        return random.choice(REPLIES["number"])

    elif any(w in text_lower for w in ["good morning", "morning", "subah", "savera"]):
        return random.choice(REPLIES["morning"])

    elif any(w in text_lower for w in ["good evening", "evening", "shaam"]):
        return random.choice(REPLIES["evening"])

    elif any(w in text_lower for w in ["good night", "night", "raat", "so raha", "so rahi", "neend"]):
        return random.choice(REPLIES["night"])

    elif any(w in text_lower for w in ["bored", "bore", "kuch nahi", "timepass", "akela", "lonely"]):
        return random.choice(REPLIES["bored"])

    elif any(w in text_lower for w in ["miss", "yaad", "yaad aaya", "yaad aayi"]):
        return random.choice(REPLIES["miss"])

    elif any(w in text_lower for w in ["thanks", "thank you", "shukriya", "dhanyawad", "ty"]):
        return random.choice(REPLIES["thanks"])

    else:
        return random.choice(REPLIES["default"])

async def start(update, context):
    name = update.effective_user.first_name or "yaar"
    await update.message.reply_text(f"Hiii {name}! 🌸 Main Shivani hoon! Kaisa hai? 😊")

async def help_command(update, context):
    await update.message.reply_text("Haha help? Bas baat karo mere se 😄🌸")

async def promote_command(update, context):
    link = random.choice(GROUP_LINKS)
    msg = random.choice(PROMO_MESSAGES).format(link=link)
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join!", url=link)]]))

async def handle_message(update, context):
    if not update.message or not update.message.text:
        return
    message = update.message
    text = message.text
    user_name = message.from_user.first_name or "yaar"
    bot_username = context.bot.username
    is_private = message.chat.type == "private"
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.username == bot_username
    is_mentioned = f"@{bot_username}" in text if bot_username else False
    should_reply = is_private or is_reply_to_bot or is_mentioned

    async def send_reply(txt):
        if random.random() < 0.15:
            link = random.choice(GROUP_LINKS)
            promo = random.choice(PROMO_MESSAGES).format(link=link)
            await message.reply_text(txt)
            await message.reply_text(promo, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Join!", url=link)]]))
        else:
            await message.reply_text(txt)

    if should_reply:
        clean = text.replace(f"@{bot_username}", "").strip()
        await send_reply(get_smart_reply(clean, user_name))
    elif not is_private:
        if random.random() < 0.40:
            await send_reply(get_smart_reply(text, user_name))
        elif random.random() < 0.10:
            link = random.choice(GROUP_LINKS)
            promo = random.choice(PROMO_MESSAGES).format(link=link)
            await message.reply_text(promo, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Join!", url=link)]]))

async def handle_new_chat(update, context):
    result = update.my_chat_member
    if result.new_chat_member.status in ["member", "administrator"]:
        chat = update.effective_chat
        link = random.choice(GROUP_LINKS)
        welcome = f"Hiii {chat.title}! 🌸 Main Shivani hoon!\nMujhse baat karo 😊\n\nEk mazedaar group:\n👉 {link}\nJoin karo! 🔥"
        try:
            await context.bot.send_message(chat_id=chat.id, text=welcome, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Join Now!", url=link)]]))
        except Exception as e:
            logger.error(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("promote", promote_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(ChatMemberHandler(handle_new_chat, ChatMemberHandler.MY_CHAT_MEMBER))
    logger.info("Shivani Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
