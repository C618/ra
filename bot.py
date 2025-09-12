import os
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# تكوين التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')
app = Flask(__name__)
bot = Bot(token=API_TOKEN)

# الحصول على Render URL
RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL', '')
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/webhook" if RENDER_EXTERNAL_URL else ""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 مرحباً! أنا بوت تحميل الفيديو. أرسل لي أي فيديو.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📥 تم استلام الفيديو! جاري المعالجة...")
        await update.message.reply_text("✅ تم معالجة الفيديو بنجاح!")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء المعالجة")

# إنشاء التطبيق
application = Application.builder().token(API_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VIDEO, handle_video))
application.initialize()

# === جميع Routes المطلوبة ===

@app.route("/")
def home():
    return "✅ Telegram Video Bot is running on Render!"

@app.route("/health")
def health_check():
    return "🟢 Healthy", 200

@app.route("/set_webhook")
def set_webhook():
    """إعداد webhook على Telegram"""
    if not WEBHOOK_URL:
        return "❌ Webhook URL not set", 500
    
    try:
        # استخدام طريقة sync لتعيين webhook
        success = bot.set_webhook(WEBHOOK_URL)
        return f"✅ Webhook set successfully!<br>URL: {WEBHOOK_URL}<br>Success: {success}"
    except Exception as e:
        return f"❌ Error setting webhook: {e}", 500

@app.route("/remove_webhook")
def remove_webhook():
    """إلغاء webhook"""
    try:
        success = bot.delete_webhook()
        return f"✅ Webhook removed: {success}"
    except Exception as e:
        return f"❌ Error removing webhook: {e}", 500

@app.route("/webhook", methods=["POST"])
def webhook():
    """معالجة webhook من Telegram"""
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), bot)
            application.update_queue.put_nowait(update)
            return "OK"
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return "Error", 500
    return "Method not allowed", 405

@app.route("/get_webhook_info")
def get_webhook_info():
    """الحصول على معلومات webhook"""
    try:
        info = bot.get_webhook_info()
        return f"Webhook Info:<br>{info}"
    except Exception as e:
        return f"Error getting webhook info: {e}", 500

if __name__ == "__main__":
    # محاولة تعيين webhook تلقائياً عند التشغيل
    if WEBHOOK_URL:
        try:
            bot.set_webhook(WEBHOOK_URL)
            logger.info(f"Webhook set to: {WEBHOOK_URL}")
        except Exception as e:
            logger.warning(f"Failed to set webhook: {e}")
    
    # تشغيل Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
