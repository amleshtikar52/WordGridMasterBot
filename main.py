from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

from config import BOT_TOKEN, BOT_OWNER_ID, GRID_NORMAL, GRID_HARD
from database import (
    games, add_score, sub_score, set_score,
    group_scores, global_scores, achievements
)
from game import create_game
from image_gen import generate_grid_image


# ================= START (DM ONLY) =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    keyboard = [
        [InlineKeyboardButton("➕ Add me to Group",
          url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📘 Help & Commands", callback_data="help")]
    ]

    await update.message.reply_photo(
        photo="https://i.imgur.com/9YQZQ9G.png",
        caption=(
            "👋 **Welcome to Word Grid!**\n\n"
            "🎮 Multiplayer word puzzle game\n"
            "➕ Add me to a group\n"
            "▶️ Use /new or /new_hard to start"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================= HELP =================
async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    text = (
        "📘 **Word Grid Commands**\n\n"
        "🎮 **Game**\n"
        "/new – Start 8×8 game\n"
        "/new_hard – Start 14×14 game\n"
        "/end – End game (Admin + Owner)\n"
        "/hint – Get hint\n\n"
        "📊 **Stats**\n"
        "/me – Your score\n"
        "/leaderboard – Group leaderboard\n"
        "/scorecard – Score image\n"
        "/achievements – Your achievements\n\n"
        "⚙️ **Utility**\n"
        "/ping – Bot status"
    )

    await q.message.reply_text(text, parse_mode="Markdown")


# ================= GAME =================
async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    games[chat_id] = create_game(GRID_NORMAL)

    img = generate_grid_image(games[chat_id]["grid"])
    await update.message.reply_photo(InputFile(img), caption="🎮 New Game Started!")


async def new_game_hard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    games[chat_id] = create_game(GRID_HARD)

    img = generate_grid_image(games[chat_id]["grid"])
    await update.message.reply_photo(InputFile(img), caption="🔥 Hard Game Started!")


async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    user = update.effective_user
    member = await context.bot.get_chat_member(chat_id, user.id)

    if user.id == BOT_OWNER_ID or member.status in ("administrator", "creator"):
        games.pop(chat_id, None)
        await update.message.reply_text("🛑 Game Ended")
    else:
        return


async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💡 Try scanning diagonally 😉")


# ================= STATS =================
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    score = global_scores.get(uid, 0)
    await update.message.reply_text(f"👤 Your Score: **{score}**", parse_mode="Markdown")


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = group_scores.get(chat_id, {})

    if not data:
        await update.message.reply_text("No data yet.")
        return

    text = "🏆 **Group Leaderboard**\n\n"
    sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

    medals = ["🥇", "🥈", "🥉"]
    for i, (uid, sc) in enumerate(sorted_users):
        medal = medals[i] if i < 3 else f"{i+1}."
        text += f"{medal} `{uid}` — {sc}\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def scorecard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    score = global_scores.get(uid, 0)

    from PIL import Image, ImageDraw
    import io

    img = Image.new("RGB", (400, 200), "white")
    d = ImageDraw.Draw(img)
    d.text((40, 80), f"Your Score: {score}", fill="black")

    bio = io.BytesIO()
    img.save(bio, "PNG")
    bio.seek(0)

    await update.message.reply_photo(InputFile(bio), caption="📊 Your Scorecard")


async def achievements_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    ach = achievements[uid] or {"No achievements yet"}
    await update.message.reply_text("🏅 Achievements:\n" + "\n".join(ach))


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")


# ================= OWNER SECRET COMMANDS =================
async def addscore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        return
    user = update.message.entities[1].user
    points = int(context.args[1])
    add_score(update.effective_chat.id, user.id, points)


async def subscore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        return
    user = update.message.entities[1].user
    points = int(context.args[1])
    sub_score(update.effective_chat.id, user.id, points)


# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(help_menu, pattern="help"))

    app.add_handler(CommandHandler("new", new_game))
    app.add_handler(CommandHandler("new_hard", new_game_hard))
    app.add_handler(CommandHandler("end", end_game))
    app.add_handler(CommandHandler("hint", hint))

    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("scorecard", scorecard))
    app.add_handler(CommandHandler("achievements", achievements_cmd))
    app.add_handler(CommandHandler("ping", ping))

    # hidden owner commands
    app.add_handler(CommandHandler("addscore", addscore))
    app.add_handler(CommandHandler("subscore", subscore))

    print("🤖 WordGridMasterBot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
