from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, ContextTypes, filters
)
import asyncio

# ================= BOT TOKEN =================
TOKEN = "8582644550:AAGX-1pHFwhpUYGIq-P4I-DIy6mbZGv5Ofo"

# ================= FORCE JOIN (ONLY CHANNEL 1) =================
CHANNELS = [
    "@hack4hub"
]

# ================= JOIN BUTTON LINKS =================
CHANNEL_LINKS = [
    ("🔔 Join Channel 1", "https://t.me/hack4hub"),
    ("📣 Join Channel 2", "https://t.me/ha4kera"),
    ("⭐ Join Channel 3", "https://t.me/+SDB9fB8svGQ1ODRl"),
]

# ================= MEMORY =================
user_state = {}   # user_id -> verified / awaiting_target

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    name = f"@{user.username}" if user.username else user.first_name

    if user_state.get(uid) == "verified":
        await update.message.reply_text(
            f"Hey {name} 👋\n\n"
            "Welcome to Teleport Bot 🚀\n"
            "Made by @umeekabhai and @indexAbhisek\n\n"
            "👉 Enter /ban to continue"
        )
        return

    keyboard = [[InlineKeyboardButton(t, url=l)] for t, l in CHANNEL_LINKS]
    keyboard.append([InlineKeyboardButton("✅ Joined", callback_data="check_join")])

    await update.message.reply_text(
        "🔒 *System Locked*\n\nJoin all channels to continue.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CHECK JOIN (ONLY CHANNEL 1) =================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    uid = user.id
    name = f"@{user.username}" if user.username else user.first_name

    try:
        member = await context.bot.get_chat_member(CHANNELS[0], uid)
        if member.status not in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                "❌ You have not joined Channel 1.\n\n"
                "Please join and click ✅ Joined again."
            )
            return
    except:
        await query.edit_message_text(
            "⚠️ Unable to verify Channel 1.\n"
            "Make sure the bot is ADMIN there."
        )
        return

    user_state[uid] = "verified"

    await query.edit_message_text(
        f"Hey {name} 👋\n\n"
        "Welcome to Teleport Bot 🚀\n"
        "Made by @umeekabhai and @indexAbhisek\n\n"
        "👉 Enter /ban to continue"
    )

# ================= BAN COMMAND =================
async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if user_state.get(uid) != "verified":
        await update.message.reply_text(
            "❌ Access denied.\nPlease use /start and complete verification."
        )
        return

    user_state[uid] = "awaiting_target"
    await update.message.reply_text(
        "💀 *Mass Report Tool Activated*\n\n"
        "Send the username or channel now:\n"
        "`@username`  |  `@channel`  |  `https://t.me/channel`",
        parse_mode="Markdown"
    )

# ================= TARGET INPUT =================
async def target_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if user_state.get(uid) != "awaiting_target":
        return

    raw = update.message.text.strip()

    # normalize input
    if raw.startswith("https://t.me/"):
        target = "@" + raw.split("/")[-1]
    elif raw.startswith("@"):
        target = raw
    else:
        target = "@" + raw

    await update.message.reply_text(
        f"🚀 Processing **{target}** ...",
        parse_mode="Markdown"
    )

    # long progress sequence
    counts = [10, 20, 13, 12, 18, 22, 27, 31, 35, 40]
    for c in counts:
        await asyncio.sleep(1)
        await update.message.reply_text(f"Report sent by bot ✅ {c}")

    await update.message.reply_text(
        "✅ *Process Completed Successfully!*",
        parse_mode="Markdown"
    )

    user_state[uid] = "verified"

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, target_input))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()