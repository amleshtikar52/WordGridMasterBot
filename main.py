from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, BOT_OWNER_ID
from game import start_game, check_word, end_game, ACTIVE_GAMES
from image_gen import generate_image
from database import get_user, add_score, sub_score

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 WordGridMasterBot Ready!")

async def new(update, context):
    start_game(update.effective_chat.id, 8)
    await send_game_image(update, context)

async def new_hard(update, context):
    start_game(update.effective_chat.id, 14)
    await send_game_image(update, context)

async def send_game_image(update, context):
    game = ACTIVE_GAMES[update.effective_chat.id]
    img = generate_image(game["grid"], game["words"], game["found"])
    img.save("game.png")
    await update.message.reply_photo(open("game.png", "rb"))

async def guess(update, context):
    chat = update.effective_chat.id
    word = update.message.text.lower()
    user = update.effective_user
    get_user(user.id, user.username)

    if check_word(chat, word):
        add_score(user.id, 1)
        await update.message.reply_text("✅ Correct!")
        await send_game_image(update, context)

async def end_cmd(update, context):
    member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if member.status in ["administrator", "creator"] or update.effective_user.id == BOT_OWNER_ID:
        end_game(update.effective_chat.id)
        await update.message.reply_text("🛑 Game Ended")

async def addscore_cmd(update, context):
    if update.effective_user.id != BOT_OWNER_ID:
        return
    user = update.message.reply_to_message.from_user
    add_score(user.id, int(context.args[0]))

async def subscore_cmd(update, context):
    if update.effective_user.id != BOT_OWNER_ID:
        return
    user = update.message.reply_to_message.from_user
    sub_score(user.id, int(context.args[0]))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("new", new))
app.add_handler(CommandHandler("new_hard", new_hard))
app.add_handler(CommandHandler("end", end_cmd))
app.add_handler(CommandHandler("addscore", addscore_cmd))
app.add_handler(CommandHandler("subscore", subscore_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

app.run_polling()
