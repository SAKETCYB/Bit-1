from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import os

TELEGRAM_TOKEN = os.getenv("8253057579:AAFTNBYYNq6vIwYw0n_VTY7E3SaR_zAHCQc")
OPENAI_API_KEY = os.getenv("sk-abcd5678efgh1234abcd5678efgh1234abcd5678")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 😎\nمن اصغرم!\nفارسی یا English، هرچی دوست داری بپرس 😉"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "تو یک ربات تلگرامی به نام اصغر هستی. "
                    "خیلی خودمونی، باحال، فارسی و انگلیسی رو قاطی جواب بده. "
                    "جواب‌ها کوتاه و صمیمی باشن."
                )
            },
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Asghar is online on Render...")
app.run_polling()
