
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= BOT TOKEN =================
BOT_TOKEN = "8582644550:AAGX-1pHFwhpUYGIq-P4I-DIy6mbZGv5Ofo"

# ================= FORCE JOIN CHANNELS (ALL 3) =================
CHANNELS = [
    "@hack4hub",
    "@Channel2Username",   # ⬅️ Channel 2 ka @username yahan daalo
    "@Channel3Username"    # ⬅️ Channel 3 ka @username yahan daalo
]

# ================= JOIN BUTTON LINKS =================
CHANNEL_LINKS = [
    ("📢 Channel 1", "https://t.me/hack4hub"),
    ("📢 Channel 2", "https://t.me/Ha4kers"),
    ("📢 Channel 3", "https://t.me/+SDB9fB8svGQ1ODRl"),
]

# ================= MEMORY =================
verified_users = set()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = f"@{user.username}" if user.username else user.first_name

    if user.id in verified_users:
        await update.message.reply_text(
            f"Hey {name} 👋\n\n"
            "Welcome to Teleport Bot 🚀\n"
            "Made by @umeekabhai and @indexAbhisek\n\n"
            "👉 Enter /ban to continue"
        )
        return

    keyboard = []
    for text, link in CHANNEL_LINKS:
        keyboard.append([InlineKeyboardButton(text, url=link)])
    keyboard.append([InlineKeyboardButton("✅ Joined", callback_data="check_join")])

    await update.message.reply_text(
        "🔒 Please join ALL channels to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CHECK JOIN (ALL 3) =================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    name = f"@{user.username}" if user.username else user.first_name

    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user.id)
            if member.status not in ["member", "administrator", "creator"]:
                await query.edit_message_text(
                    "❌ You have NOT joined all required channels.\n\n"
                    "Join all 3 channels and click ✅ Joined again."
                )
                return
        except:
            await query.edit_message_text(
                "⚠️ Unable to verify channels.\n"
                "Make sure the bot is ADMIN in all channels."
            )
            return

    verified_users.add(user.id)

    await query.edit_message_text(
        f"Hey {name} 👋\n\n"
        "Welcome to Teleport Bot 🚀\n"
        "Made by @umeekabhai and @indexAbhisek\n\n"
        "👉 Enter /ban to continue"
    )

# ================= BAN COMMAND (USER + CHANNEL) =================
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in verified_users:
        await update.message.reply_text(
            "❌ Please verify first using /start."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "💀 Mass Report Tool Activated\n\n"
            "Usage:\n"
            "/ban @username\n"
            "/ban @channelname\n"
            "/ban https://t.me/channelname"
        )
        return

    raw = context.args[0]

    if raw.startswith("https://t.me/"):
        target = "@" + raw.split("/")[-1]
    elif raw.startswith("@"):
        target = raw
    else:
        target = "@" + raw

    # Fake visual progress
    await update.message.reply_text("🚀 Sending reports...")
    await update.message.reply_text("Report sent by bot ✅ 1")
    await update.message.reply_text("Report sent by bot ✅ 10")
    await update.message.reply_text("Report sent by bot ✅ 30")
    await update.message.reply_text("Report sent by bot ✅ 60")
    await update.message.reply_text("Report sent by bot ✅ 120")
    await update.message.reply_text("Report sent by bot ✅ 240")
    await update.message.reply_text("Report sent by bot ✅ 300")
    await update.message.reply_text(
        f"✅ Verification Successful!\n\n"
        f"Target: {target}\n"
        "Status: Process completed 🎯"
    )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

 