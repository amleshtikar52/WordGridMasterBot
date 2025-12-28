from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, BOT_OWNER_ID, GRID_NORMAL, GRID_HARD, POINTS_PER_WORD
from database import add_score, get_score, get_leaderboard
from game import start_game, end_game, get_game
from image_gen import generate_image
import random

WORD_POOL = [
    "OXYGEN","SOUND","LIGHT","PLANT","STONE","EARTH","WATER",
    "POWER","SHADOW","FIRE","METAL","ENERGY","SPACE","WIND"
]

# ---------- START (DM ONLY) ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hello {user}!\n\n"
        "I'm a Word Grid Bot 🧩\n\n"
        "➤ Add me to a group\n"
        "➤ Use /new or /new_hard to start game\n\n"
        "🎯 Everyone in the group can play together!"
    )

# ---------- NEW GAME ----------
async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    start_game(chat_id, GRID_NORMAL)

    words = random.sample(WORD_POOL, 3)
    get_game(chat_id)["words"] = words

    img = generate_image(GRID_NORMAL, words)
    await update.message.reply_photo(photo=img)

# ---------- HARD ----------
async def new_hard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    start_game(chat_id, GRID_HARD)

    words = random.sample(WORD_POOL, 5)
    get_game(chat_id)["words"] = words

    img = generate_image(GRID_HARD, words)
    await update.message.reply_photo(photo=img)

# ---------- WORD GUESS ----------
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = get_game(chat_id)
    if not game:
        return

    word = update.message.text.upper()
    if word in game["found"]:
        await update.message.reply_text("⚠️ This word is already found")
        return

    if word in game["words"]:
        game["found"].add(word)
        add_score(update.effective_user.id, POINTS_PER_WORD)
        await update.message.reply_text(
            f"✅ @{update.effective_user.username} found {word} (+5 points)"
        )

# ---------- ME ----------
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = get_score(update.effective_user.id)
    await update.message.reply_text(f"🏆 Your Score: {score}")

# ---------- LEADERBOARD ----------
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lb = get_leaderboard()
    text = "🏆 LEADERBOARD\n\n"
    for i, (uid, score) in enumerate(lb, 1):
        text += f"{i}. {score}\n"
    await update.message.reply_text(text)

# ---------- END ----------
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await update.effective_chat.get_member(user.id)

    if user.id == BOT_OWNER_ID or member.status in ["administrator", "creator"]:
        end_game(update.effective_chat.id)
        await update.message.reply_text("❌ Game Ended")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_game))
    app.add_handler(CommandHandler("new_hard", new_hard))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("end", end))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

    app.run_polling()

if __name__ == "__main__":
    main()
