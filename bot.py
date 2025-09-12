import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import asyncio
from threading import Thread

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت - تأكد من إضافته في متغيرات البيئة على Render
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')

# تطبيق Flask لربط المنفذ
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Video Bot is running on Web Service!"

@app.route('/health')
def health_check():
    return "🟢 Healthy", 200

# handlers للبوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 مرحباً! أنا بوت تحميل الفيديو. أرسل لي أي فيديو وسأقوم بمعالجته.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📥 تم استلام الفيديو! جاري المعالجة...")
        
        # محاكاة معالجة الفيديو
        await asyncio.sleep(2)
        await update.message.reply_text("✅ تم معالجة الفيديو بنجاح!")
        
    except Exception as e:
        logger.error(f"Error handling video: {e}")
        await update.message.reply_text("❌ عذراً، حدث خطأ أثناء معالجة الفيديو.")

# إنشاء وتكوين application تيليجرام
def setup_bot():
    application = Application.builder().token(API_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # بدء البوت باستخدام webhook
    try:
        # الحصول على URL من Render
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}/{API_TOKEN}"
        
        # استخدام webhook للتوافق مع Web Service
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 10000)),
            webhook_url=webhook_url,
            drop_pending_updates=True
        )
    except Exception as e:
        logger.error(f"Webhook setup failed: {e}")
        # Fallback إلى polling
        application.run_polling()

# تشغيل البوت في thread منفصل
def run_bot():
    setup_bot()

if __name__ == '__main__':
    # بدء البوت في thread منفصل
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # بدء Flask على المنفذ المطلوب
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
