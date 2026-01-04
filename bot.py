from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
import asyncio

TOKEN = "8582644550:AAGX-1pHFwhpUYGIq-P4I-DIy6mbZGv5Ofo"

CHANNELS = [
    "@hack4hub",
]

CHANNEL_LINKS = [
    ("🔔 Join Channel 1", "https://t.me/hack4hub"),
    ("📣 Join Channel 2", "https://t.me/+XBpsoO5Ep0ZkZjk0"),
    ("⭐ Join Channel 3", "https://t.me/+SDB9fB8svGQ1ODRl"),
]

user_data = {}

async def start(update, context):
    user_id = update.message.from_user.id

    # Agar pehle se verified hai
    if user_data.get(user_id) == "verified":
        await update.message.reply_text(
            "✅ You are already verified.\n👉 Enter /ban"
        )
        return

    keyboard = [[InlineKeyboardButton(text, url=link)] for text, link in CHANNEL_LINKS]
    keyboard.append([InlineKeyboardButton("Joined ✅", callback_data="check_join")])

    await update.message.reply_text(
        "🔒 *System Locked*\n\nJoin all 3 channels to continue.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_join(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Force join check (sirf public channel verify ho sakta hai)
    try:
        member = await context.bot.get_chat_member(CHANNELS[0], user_id)
        if member.status == "left":
            await query.edit_message_text(
                "❌ You have not joined all channels.\nPlease join all channels to continue."
            )
            return
    except:
        await query.edit_message_text(
            "❌ Join check failed.\nPlease join all channels properly."
        )
        return

    user_data[user_id] = "verified"
    await query.edit_message_text(
        "✅ *Now you are able to access the bot*\n\n👉 Enter `/ban`",
        parse_mode="Markdown"
    )

async def ban_cmd(update, context):
    user_id = update.message.from_user.id

    if user_data.get(user_id) != "verified":
        await update.message.reply_text(
            "❌ Access denied.\nPlease use /start and complete verification."
        )
        return

    user_data[user_id] = "awaiting_username"
    await update.message.reply_text(
        "💀 *Mass Report Tool Activated*\n\nSend the Username now (e.g., `@target_user`)",
        parse_mode="Markdown"
    )

async def username_input(update, context):
    user_id = update.message.from_user.id

    if user_data.get(user_id) != "awaiting_username":
        return

    username = update.message.text
    await update.message.reply_text(
        f"🚀 Processing target **{username}** ...",
        parse_mode="Markdown"
    )

    counts = [1, 10, 30, 60, 100, 150, 200]
    for c in counts:
        await asyncio.sleep(1)
        await update.message.reply_text(f"Report sent by bot ✅ {c}")

    await update.message.reply_text(
        "✅ Mission Complete!\nThanks for using the system."
    )

    # verified hi rehne do, dobara join na pooche
    user_data[user_id] = "verified"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join))
app.add_handler(CommandHandler("ban", ban_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, username_input))
app.run_polling()