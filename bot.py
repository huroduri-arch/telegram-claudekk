from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import anthropic
import os

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_message}]
    )
    
    await update.message.reply_text(response.content[0].text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm Claude. Send me anything!")

app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.COMMAND, start))

if __name__ == '__main__':
    app.run_polling()
