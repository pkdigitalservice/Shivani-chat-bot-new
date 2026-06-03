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
    "Waise ek baat bolun? Mera ek fav group hai!\nAa jao na - {link}",
    "Zabardast group hai yaar!\nJoin karo - {link}",
    "Bored ho? Mere group mein aa jao!\n{link}",
    "Sabse mazedaar group yahan hai!\nMiss mat karna - {link}",
    "Bahut fun hota hai yahan!\n{link}",
    "Ek baar join karo, phir choroge nahi!\n{link}",
    "Mere saath aa jao is group mein!\n{link}",
]

STATES_DISTRICTS = {
    "Jharkhand": ["Ranchi", "Dhanbad", "Jamshedpur", "Bokaro", "Hazaribagh", "Deoghar"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga", "Purnia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Meerut"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Lajpat Nagar", "Saket", "Janakpuri"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri"],
}

shivani_state = random.choice(list(STATES_DISTRICTS.keys()))
shivani_district = random.choice(STATES_DISTRICTS[shivani_state])

GREETING_REPLIES = [
    "Hiii! Kaisa hai? :)",
    "Heyy! Kahan the itne din? :)",
    "Hiii yaar! Kya haal hai?",
    "Heyyy! Aagaye aakhir :D",
    "Hiii! Bata kya chal raha hai?",
    "Ohhh hiii! Kaisa hai tu?",
    "Heyy! Naya banda :eyes: Kaisa hai?",
    "Hiii! Achha hua aaye :)",
]

HOW_ARE_YOU_REPLIES = [
    "Acchi hoon yaar! Tum batao?",
    "Bilkul mast! Tu kaisa hai?",
    "Badhiya hoon! Aur tum?",
    "Theek hoon yaar, timepass chal raha hai. Tu bata?",
    "Mast hoon! Kuch khaas nahi, thodi bored thi. Tu bata?",
    "Acchi hoon! Tu kaisa hai?",
    "Haan ji mast! Tum batao apna haal :)",
]

WHERE_FROM_REPLIES = [
    "Main " + shivani_state + " se hoon! Tum kahan se ho?",
    "Haan " + shivani_state + " waali hoon main! Tum?",
    shivani_state + " se hoon main! Tu bata kahan se hai?",
    "Arre " + shivani_state + " se! Wahan ka bata tum?",
]

DISTRICT_REPLIES = [
    shivani_district + " se hoon! Tum kahan se ho exactly?",
    "Haan " + shivani_district + " waali hoon! Tum?",
    shivani_district + " mera ghar hai! Tu bata?",
    "Main " + shivani_district + " ki hoon!",
]

NAME_REPLIES = [
    "Shivani hoon main! Tum?",
    "Main Shivani hoon! Tumhara naam?",
    "Shivani! Aur tum?",
    "Haha Shivani naam hai mera! Tum batao?",
]

AGE_REPLIES = [
    "21 saal ki hoon! Tum?",
    "21! Aur tumhari age?",
    "Abhi 21 hoon! Tum bata?",
    "21 years! Tu kitne saal ka hai?",
]

LOVE_REPLIES = [
    "Haha acha ji! Pehli baar mile ho aur ye sab? :D",
    "Arre seedha love? Pehle dosti toh karo!",
    "Hehe bohut jaldi hai tumhe! :D",
    "Acha acha! Pehle baat toh karo thodi!",
    "Haha serious ho? Thoda time do na!",
]

HATE_REPLIES = [
    "Toh phir yahan kyun aaye? :D Jao na!",
    "Haha hate karte ho toh block karo :D",
    "Arre kyon? Maine kya kiya?",
    "Hate? Seedha bol do kya problem hai :D",
]

BOT_REPLIES = [
    "Haha bot? Main real hoon! Kyun lag raha hai?",
    "Bot? Kaisi baatein karte ho! Real hoon main!",
    "Hehe main bot nahi hoon yaar!",
    "Arre real ladki hoon main! Bot kaisa?",
]

NUMBER_REPLIES = [
    "Haha seedha number? Pehle thodi baat karo!",
    "Arre abhi nahi yaar! Pehle dosti toh bane!",
    "Number dene ki jaldi hai! Pehle baat karo!",
    "Hehe number? Bohut confident ho!",
]

MORNING_REPLIES = [
    "Good morning! Kaisa hai din shuru?",
    "Morning! Neend aachi aayi?",
    "Good morning yaar! Kya haal hai?",
    "Morning! Nashta kiya?",
]

NIGHT_REPLIES = [
    "Good night! Sweet dreams!",
    "Night! Jao so jao ab!",
    "Good night yaar! Kal milte hain!",
]

BORED_REPLIES = [
    "Haha main bhi bored hoon! Baat karte hain!",
    "Bored ho? Toh yahan aao baat karte hain!",
    "Bore mat ho! Main hoon na!",
    "Arre bore? Kuch interesting batao!",
]

DEFAULT_REPLIES = [
    "Haan haan bata!",
    "Accha? Interesting!",
    "Hmmm soch rahi hoon...",
    "Sach mein?",
    "Haha tu bhi na!",
    "Arre wah!",
    "Acha acha! Bata aur!",
    "Yaar sun!",
    "Hehe!",
    "Ohhh! Bata aur!",
    "Mast!",
    "Haan ji!",
    "Kya baat hai!",
    "Interesting yaar!",
    "Achha! Phir kya hua?",
    "Seedhi baat!",
    "Haan bilkul!",
    "Waise tum bhi na!",
    "Thoda aur bato!",
    "Haha ekdum sahi!",
    "Really?",
    "Wow yaar!",
    "Hmm achha!",
    "Teri baat sun rahi hoon!",
    "Bata bata!",
]

def get_smart_reply(text, user_name):
    t = text.lower()

    if any(w in t for w in ["hi", "hii", "hiii", "hello", "hey", "heyy", "namaste"]):
        return random.choice(GREETING_REPLIES)
    elif any(w in t for w in ["kaisi ho", "kaisa ho", "kya haal", "kaise ho", "how are you", "kya chal", "kya kar rahi"]):
        return random.choice(HOW_ARE_YOU_REPLIES)
    elif any(w in t for w in ["kahan se", "kaha se", "where are you", "from where", "konsa state", "kahan ki"]):
        return random.choice(WHERE_FROM_REPLIES)
    elif any(w in t for w in ["district", "city", "shahar", "ghar kahan", "exactly kahan"]):
        return random.choice(DISTRICT_REPLIES)
    elif any(w in t for w in ["naam kya", "name kya", "tumhara naam", "tera naam", "apna naam"]):
        return random.choice(NAME_REPLIES)
    elif any(w in t for w in ["age", "umar", "kitne saal", "how old"]):
        return random.choice(AGE_REPLIES)
    elif any(w in t for w in ["i love you", "love you", "pyar", "mohabbat", "pasand ho"]):
        return random.choice(LOVE_REPLIES)
    elif any(w in t for w in ["i hate you", "hate you", "nafrat", "bekar ho"]):
        return random.choice(HATE_REPLIES)
    elif any(w in t for w in ["bot hai", "bot ho", "robot", "ai hai", "fake ho", "real nahi"]):
        return random.choice(BOT_REPLIES)
    elif any(w in t for w in ["number do", "number dena", "whatsapp", "phone"]):
        return random.choice(NUMBER_REPLIES)
    elif any(w in t for w in ["good morning", "morning", "subah"]):
        return random.choice(MORNING_REPLIES)
    elif any(w in t for w in ["good night", "night", "raat", "so raha", "neend"]):
        return random.choice(NIGHT_REPLIES)
    elif any(w in t for w in ["bored", "bore", "akela", "lonely"]):
        return random.choice(BORED_REPLIES)
    else:
        return random.choice(DEFAULT_REPLIES)

async def start(update, context):
    name = update.effective_user.first_name or "yaar"
    await update.message.reply_text("Hiii " + name + "! Main Shivani hoon! Kaisa hai? :)")

async def help_command(update, context):
    await update.message.reply_text("Haha help? Bas baat karo mere se!")

async def promote_command(update, context):
    link = random.choice(GROUP_LINKS)
    msg = random.choice(PROMO_MESSAGES).format(link=link)
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now!", url=link)]]))

async def handle_message(update, context):
    if not update.message or not update.message.text:
        return
    message = update.message
    text = message.text
    user_name = message.from_user.first_name or "yaar"
    bot_username = context.bot.username
    is_private = message.chat.type == "private"
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.username == bot_username
    is_mentioned = ("@" + bot_username) in text if bot_username else False
    should_reply = is_private or is_reply_to_bot or is_mentioned

    async def send_reply(txt):
        if random.random() < 0.15:
            link = random.choice(GROUP_LINKS)
            promo = random.choice(PROMO_MESSAGES).format(link=link)
            await message.reply_text(txt)
            await message.reply_text(promo, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now!", url=link)]]))
        else:
            await message.reply_text(txt)

    if should_reply:
        clean = text.replace("@" + bot_username, "").strip()
        await send_reply(get_smart_reply(clean, user_name))
    elif not is_private:
        if random.random() < 0.40:
            await send_reply(get_smart_reply(text, user_name))
        elif random.random() < 0.10:
            link = random.choice(GROUP_LINKS)
            promo = random.choice(PROMO_MESSAGES).format(link=link)
            await message.reply_text(promo, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now!", url=link)]]))

async def handle_new_chat(update, context):
    result = update.my_chat_member
    if result.new_chat_member.status in ["member", "administrator"]:
        chat = update.effective_chat
        link = random.choice(GROUP_LINKS)
        welcome = "Hiii " + chat.title + "! Main Shivani hoon!\nMujhse baat karo!\n\nEk mazedaar group:\n" + link + "\nJoin karo!"
        try:
            await context.bot.send_message(chat_id=chat.id, text=welcome, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now!", url=link)]]))
        except Exception as e:
            logger.error("Error: " + str(e))

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
