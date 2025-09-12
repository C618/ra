import os
import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')

# تطبيق Flask
app = Flask(__name__)

# إنشاء كائنات البوت
bot = Bot(token=API_TOKEN)

# الحصول على Render URL
RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL', '')
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/webhook" if RENDER_EXTERNAL_URL else ""

# === Handlers للبوت ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 مرحباً! أنا بوت تحميل الفيديو. أرسل لي أي فيديو وسأقوم بمعالجته.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📥 تم استلام الفيديو! جاري المعالجة...")
        # محاكاة المعالجة
        await asyncio.sleep(1)
        await update.message.reply_text("✅ تم معالجة الفيديو بنجاح!")
    except Exception as e:
        logger.error(f"Error handling video: {e}")
        await update.message.reply_text("❌ عذراً، حدث خطأ أثناء المعالجة.")

# === إنشاء وتهيئة التطبيق ===
def create_application():
    """إنشاء وتهيئة تطبيق تيليجرام"""
    application = Application.builder().token(API_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # تهيئة التطبيق
    application.initialize()
    
    return application

# إنشاء التطبيق
application = create_application()

# === Flask route لـ webhook ===
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            # معالجة webhook
            update = Update.de_json(request.get_json(force=True), bot)
            
            # معالجة التحديث بشكل غير متزامن
            async def process_update_async():
                await application.process_update(update)
            
            asyncio.run(process_update_async())
            return "OK"
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return "Error", 500
    return "Method not allowed", 405

# === إعداد webhook على Telegram ===
@app.route("/set_webhook")
def set_webhook():
    if not WEBHOOK_URL:
        return "Webhook URL not set", 500
    
    try:
        success = asyncio.run(bot.set_webhook(WEBHOOK_URL))
        return f"✅ Webhook set: {success}\nURL: {WEBHOOK_URL}"
    except Exception as e:
        return f"❌ Error setting webhook: {e}", 500

# === إلغاء webhook ===
@app.route("/remove_webhook")
def remove_webhook():
    try:
        success = asyncio.run(bot.delete_webhook())
        return f"✅ Webhook removed: {success}"
    except Exception as e:
        return f"❌ Error removing webhook: {e}", 500

# === صفحة رئيسية ===
@app.route("/")
def home():
    return "✅ Telegram Video Bot is running on Render!"

# === تشغيل التطبيق ===
if __name__ == "__main__":
    # إعداد webhook تلقائياً عند التشغيل
    if WEBHOOK_URL:
        try:
            asyncio.run(bot.set_webhook(WEBHOOK_URL))
            logger.info(f"Webhook set to: {WEBHOOK_URL}")
        except Exception as e:
            logger.warning(f"Failed to set webhook: {e}")
    
    # تشغيل Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
