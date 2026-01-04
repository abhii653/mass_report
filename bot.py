from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
import asyncio

TOKEN = "8582644550:AAGX-1pHFwhpUYGIq-P4I-DIy6mbZGv5Ofo"

CHANNEL_PUBLIC = "@hack4hub"

user_state = {}

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🔔 Join Channel 1", url="https://t.me/hack4hub")],
        [InlineKeyboardButton("📣 Join Channel 2", url="https://t.me/+XBpsoO5Ep0ZkZjk0")],
        [InlineKeyboardButton("⭐ Join Channel 3", url="https://t.me/+SDB9fB8svGQ1ODRl")],
        [InlineKeyboardButton("Joined ✅", callback_data="check")]
    ]
    await update.message.reply_text(
        "🔒 *System Locked!*\n\nJoin all channels to unlock.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_join(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_PUBLIC, user_id)
        if member.status == "left":
            await query.edit_message_text("❌ Pehle Channel 1 join karo!")
            return
    except:
        pass

    await query.edit_message_text(
        "✅ *Verification Successful!*\n\n👉 Enter `/ban`",
        parse_mode="Markdown"
    )
    user_state[user_id] = "verified"

async def ban_cmd(update, context):
    user_id = update.message.from_user.id
    if user_state.get(user_id) != "verified":
        await update.message.reply_text("❌ Pehle verification complete karo.")
        return

    user_state[user_id] = "awaiting_username"
    await update.message.reply_text(
        "💀 *Mass Report Tool Activated*\n\nSend the *Username* now (e.g., `@target_user`)",
        parse_mode="Markdown"
    )

async def username_input(update, context):
    user_id = update.message.from_user.id
    if user_state.get(user_id) != "awaiting_username":
        return

    username = update.message.text
    await update.message.reply_text(f"🚀 Locking target **{username}** ...", parse_mode="Markdown")

    counts = [1, 10, 30, 60, 100, 150, 200, 250, 300]
    for c in counts:
        await asyncio.sleep(1)
        await update.message.reply_text(f"Report sent by bot ✅ {c}")

    await update.message.reply_text(
        f"✅ *Mission Complete!*\n\n{counts[-1]} Reports sent to {username}",
        parse_mode="Markdown"
    )

    user_state[user_id] = "done"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join))
app.add_handler(CommandHandler("ban", ban_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, username_input))
app.run_polling()