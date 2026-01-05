from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================= BOT TOKEN =================
BOT_TOKEN = "8582644550:AAGX-1pHFwhpUYGIq-P4I-DIy6mbZGv5Ofo"

# ================= CHANNELS =================
# Public channel usernames ONLY (bot must be admin)
CHANNELS = [
    "@hack4hub"
]

# Join links (private/public both allowed)
CHANNEL_LINKS = [
    ("📢 Channel 1", "https://t.me/hack4hub"),
    ("📢 Channel 2", "https://t.me/+XBpsoO5Ep0ZkZjk0"),
    ("📢 Channel 3", "https://t.me/+SDB9fB8svGQ1ODRl"),
]

# ================= MEMORY =================
# (restart hone par reset ho jaayega)
verified_users = set()

# ================= START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = f"@{user.username}" if user.username else user.first_name

    # Agar user pehle se verified hai
    if user.id in verified_users:
        await update.message.reply_text(
            f"Hey {name} 👋\n\n"
            "Welcome to Teleport Bot 🚀\n"
            "Made by @umeekabhai and @indexAbhisek\n\n"
            "👉 Enter /ban to continue"
        )
        return

    # Join buttons
    keyboard = []
    for text, link in CHANNEL_LINKS:
        keyboard.append([InlineKeyboardButton(text, url=link)])

    keyboard.append([InlineKeyboardButton("✅ Joined", callback_data="check_join")])

    await update.message.reply_text(
        "🔒 Please join all channels to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CHECK JOIN =================
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    name = f"@{user.username}" if user.username else user.first_name

    # Sirf PUBLIC channels verify honge
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user.id)
            if member.status not in ["member", "administrator", "creator"]:
                await query.edit_message_text(
                    "❌ You have not joined the required channel.\n\n"
                    "Please join and click ✅ Joined again."
                )
                return
        except:
            await query.edit_message_text(
                "⚠️ Unable to verify channel.\n"
                "Make sure the bot is admin in the channel."
            )
            return

    # Verified
    verified_users.add(user.id)

    await query.edit_message_text(
        f"Hey {name} 👋\n\n"
        "Welcome to Teleport Bot 🚀\n"
        "Made by @umeekabhai and @indexAbhisek\n\n"
        "👉 Enter /ban to continue"
    )

# ================= FAKE BAN COMMAND =================
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in verified_users:
        await update.message.reply_text(
            "❌ You are not verified yet.\n"
            "Please use /start and complete verification first."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "💀 Mass Report Tool Activated\n\n"
            "Send the username now (e.g., /ban @target_user)"
        )
        return

    target = context.args[0]

    # Fake progress messages
    await update.message.reply_text("🚀 Sending reports...")
    await update.message.reply_text("Report sent by bot ✅ 1")
    await update.message.reply_text("Report sent by bot ✅ 10")
    await update.message.reply_text("Report sent by bot ✅ 30")

    await update.message.reply_text(
        f"✅ Verification Successful!\n\n"
        f"Target: {target}\n"
        "Status: Reports sent successfully 🎯"
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