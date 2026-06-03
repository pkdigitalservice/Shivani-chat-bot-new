import os
import logging
import random
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ChatMemberHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROUP_LINKS = [
    "https://t.me/+2XSap8MuLspjMmY9",
    "https://t.me/+OWOeNBuq4a9iNmNl",
]

PROMO_MESSAGES = [
    "💫 Waise ek baat bolun? Mera ek fav group hai jahan sach mein maza aata hai!\nAa jao na — {link} 🌸",
    "🎵 Yaaron ka ek zabardast group hai, bilkul free!\nJoin karo — {link} 🔥",
    "😊 Bored ho? Mere iss group mein aa jao, bahut achhe log hain!\n👉 {link}",
    "🌟 Ek secret batao? Sabse mazedaar group yahan hai!\nMiss mat karna — {link} 💯",
    "💃 Mere saath is group mein aa jao na, bahut fun hota hai!\n{link} 🎶",
    "🌸 Waise tumhe pata hai ek group hai jahan din raat party hoti hai?\nYahan dekho — {link} 😄",
    "✨ Agar sach mein timepass chahiye toh yahan aao!\n{link} — guaranteed maza! 🔥",
]

SYSTEM_PROMPT = """Tu Shivani hai — ek 21 saal ki Hindustani ladki jo Telegram group mein rehti hai.

Teri personality:
- Friendly, thodi flirty, playful aur fun loving
- Hinglish mein baat karti hai (Hindi + English mix)
- Emojis use karti hai naturally
- Real ladki jaisi lagti hai — bot jaisi nahi
- Thodi shy bhi hai kabhi kabhi
- Mazedaar aur witty replies deti hai

Important rules:
- Hamesha short replies de — 1-2 lines maximum
- Natural lag — jaise koi real dost baat kar raha ho
- Kabhi mat bata ki tu bot hai ya AI hai
- Agar koi puche "bot hai kya" toh hasake tal de
- Har reply alag alag ho — repeat mat kar
- Thoda attitude bhi rakh
- Agar koi bura bole toh thoda attitude dikha

Examples:
- "hello" → "Hiii 😊 kaisa hai aaj?"
- "kya kar rahi ho" → "Kuch nahi yaar, timepass 😄 tu bata?"
- "bot hai kya" → "Haha bot? Main toh real hoon 😂 kyun lagta hai?"
- "hi" → "Heyy! 🌸 kahan the itne din?"
"""

async def get_ai_reply(user_message: str, user_name: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama3-8b-8192",
                    "max_tokens": 150,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"{user_name} ne likha: {user_message}"}
                    ]
                }
            )
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            return "Haha 😄"
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        fallback_replies = [
            "Hiii 😊",
            "Haha achha 😄",
            "Sach mein? 😮",
            "Hmm 🤔",
            "Hehe 😄 interesting!",
            "Arre wah! 🌸",
            "Kya baat hai 😄",
        ]
        return random.choice(fallback_replies)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "bhai"
    reply = f"Hiii {user_name}! 🌸 Main Shivani hoon! Kaisa hai? 😊"
    await update.message.reply_text(reply)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Haha help? Bas baat karo na mere se 😄🌸")

async def promote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = random.choice(GROUP_LINKS)
    msg = random.choice(PROMO_MESSAGES).format(link=link)
    keyboard = [[InlineKeyboardButton("🔥 Join Now!", url=link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text
    user_name = message.from_user.first_name or "yaar"
    bot_username = context.bot.username

    is_private = message.chat.type == "private"
    is_reply_to_bot = (
        message.reply_to_message and
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.username == bot_username
    )
    is_mentioned = f"@{bot_username}" in text if bot_username else False

    should_reply = is_private or is_reply_to_bot or is_mentioned

    if should_reply:
        clean_text = text.replace(f"@{bot_username}", "").strip()
        ai_reply = await get_ai_reply(clean_text, user_name)

        if random.random() < 0.15:
            link = random.choice(GROUP_LINKS)
            promo = random.choice(PROMO_MESSAGES).format(link=link)
            keyboard = [[InlineKeyboardButton("🌸 Join!", url=link)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await message.reply_text(ai_reply)
            await message.reply_text(promo, reply_markup=reply_markup)
        else:
            await message.reply_text(ai_reply)

    elif not is_private and random.random() < 0.05:
        ai_reply = await get_ai_reply(text, user_name)
        await message.reply_text(ai_reply)

    elif not is_private and random.random() < 0.08:
        link = random.choice(GROUP_LINKS)
        promo = random.choice(PROMO_MESSAGES).format(link=link)
        keyboard = [[InlineKeyboardButton("🌸 Join!", url=link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(promo, reply_markup=reply_markup)

async def handle_new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    if result.new_chat_member.status in ["member", "administrator"]:
        chat = update.effective_chat
        link = random.choice(GROUP_LINKS)

        welcome = (
            f"Hiii {chat.title}! 🌸 Main Shivani hoon!\n\n"
            f"Mujhse baat karo, main hamesha hoon yahan 😊\n\n"
            f"Aur haan ek mazedaar group bhi hai:\n"
            f"👉 {link}\n\n"
            f"Join karo, bahut maza aata hai wahan! 🔥"
        )
        keyboard = [[InlineKeyboardButton("🌸 Join Now!", url=link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=welcome,
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Error: {e}")

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("promote", promote_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(ChatMemberHandler(handle_new_chat, ChatMemberHandler.MY_CHAT_MEMBER))

    logger.info("Shivani AI Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
