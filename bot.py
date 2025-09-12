import os
import logging
from telegram import Bot
from flask import Flask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')
app = Flask(__name__)
bot = Bot(token=API_TOKEN)

@app.route("/")
def home():
    return "✅ Bot is running!"

@app.route("/set_webhook")
def set_webhook():
    try:
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}/webhook"
        success = bot.set_webhook(webhook_url)
        return f"✅ Webhook set!<br>URL: {webhook_url}<br>Success: {success}"
    except Exception as e:
        return f"❌ Error: {e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
