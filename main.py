import os
import uuid
from flask import Flask, send_file, abort
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.constants import ParseMode
import asyncio

TOKEN = "8281942189:AAGpg2C1w_Jviv2i5ADLABlvQGVcXtBVaxs"
ADMIN_ID = 8296875526

app = Flask(__name__)
FILES = {}

@app.route("/")
def home():
    return "Uploader Bot is Running!"

@app.route("/d/<file_id>")
def download(file_id):
    if file_id not in FILES:
        return abort(404)

    filepath = FILES[file_id]
    try:
        resp = send_file(filepath, as_attachment=True)
    except:
        return abort(404)

    os.remove(filepath)
    del FILES[file_id]
    return resp


async def start(update: Update, context):
    await update.message.reply_text("سلام! فایل کانفیگت رو بفرست تا لینک یک‌بار مصرف بسازم.")

async def handle_file(update: Update, context):
    if update.message.from_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ فقط ادمین اجازه آپلود دارد")

    file = update.message.document
    if not file:
        return await update.message.reply_text("فقط فایل بفرست.")

    file_id = str(uuid.uuid4())
    new_path = f"file_{file_id}.txt"

    file_obj = await file.get_file()
    await file_obj.download_to_drive(new_path)

    FILES[file_id] = new_path

    link = f"https://{os.environ.get('RENDER_EXTERNAL_URL').replace('https://','')}/d/{file_id}"

    await update.message.reply_text(
        f"✅ **لینک یک‌بار مصرف ساخته شد:**\n\n{link}\n\nبعد از اولین دانلود حذف میشود.",
        parse_mode=ParseMode.MARKDOWN
    )


async def main():
    tg = ApplicationBuilder().token(TOKEN).build()

    tg.add_handler(CommandHandler("start", start))
    tg.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    await tg.initialize()
    await tg.start()
    await tg.updater.start_polling()
    await tg.updater.idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=10000)
