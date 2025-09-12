import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from uuid import uuid4
from flask import Flask

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إنشاء تطبيق Flask لربط المنفذ
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Video Bot is running!"

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا بوت تحميل الفيديو. أرسل لي أي فيديو وسأقوم بتنزيله.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        video_file = await update.message.video.get_file()
        file_name = f"{uuid4().hex}.mp4"
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        
        await video_file.download_to_drive(file_path)
        
        await update.message.reply_text(
            f"تم تنزيل الفيديو بنجاح!\n"
            f"الحجم: {os.path.getsize(file_path)} بايت"
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة الفيديو.")

def main():
    # تشغيل تطبيق Flask على المنفذ المطلوب
    port = int(os.environ.get('PORT', 10000))
    
    # تشغيل البوت في thread منفصل
    from threading import Thread
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل Flask
    app.run(host='0.0.0.0', port=port)

def run_bot():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.run_polling()

if __name__ == '__main__':
    main()
