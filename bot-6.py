import os
import logging
import random
import urllib.request
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GROUP_LINKS = ["https://t.me/+2XSap8MuLspjMmY9", "https://t.me/+OWOeNBuq4a9iNmNl"]

PROMO_MESSAGES = [
    "💫 Waise ek baat bolun? Mera ek fav group hai!\nAa jao na — {link} 🌸",
    "🎵 Zabardast group hai, bilkul free!\nJoin karo — {link} 🔥",
    "😊 Bored ho? Mere group mein aa jao!\n👉 {link}",
    "🌟 Sabse mazedaar group yahan hai!\nMiss mat karna — {link} 💯",
    "💃 Bahut fun hota hai yahan!\n{link} 🎶",
]

SYSTEM_PROMPT = """Tu Shivani hai — ek 21 saal ki Hindustani ladki.
Hinglish mein baat kar. Emojis use kar. Real ladki jaisi lag.
Short replies de — 1-2 lines max.
Kabhi mat bata ki tu bot hai.
Attitude rakh thoda. Har reply alag ho."""

FALLBACKS = [
    "Haha 😄 sach mein?", "Arre wah! 🌸", "Haan haan bata! 👀",
    "Hmm interesting 🤔", "Hehe tu bhi na 😂", "Accha? Phir? 😄",
    "Mast! chal raha hai? 🌸", "Ohhh 😮 bata aur!", "Yaar sun 😄",
    "Hiii! kya haal? 😊", "Sach mein? 😮", "Haha acha acha 😄",
]

def get_ai_reply(user_message, user_name):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        prompt = f"{SYSTEM_PROMPT}\n\n{user_name}: {user_message}\nShivani:"
        data = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 80, "temperature": 0.9}}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
            reply = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            if reply:
                return reply
    except Exception as e:
        logger.error(f"Gemini error: {e}")
    return random.choice(FALLBACKS)

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
        await send_reply(get_ai_reply(clean, user_name))
    elif not is_private:
        if random.random() < 0.40:
            await send_reply(get_ai_reply(text, user_name))
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
