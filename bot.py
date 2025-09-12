import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تكوين التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 مرحباً! أرسل لي فيديو.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ تم استلام الفيديو!")

def main():
    # إنشاء event loop جديد
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # استخدام polling مباشرة
    application.run_polling()

if __name__ == '__main__':
    main()
