import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)

from flask import Flask, request

# -------------------------------
# إعداد البوت
# -------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ضع التوكن في Environment Variables داخل Render
PORT = int(os.environ.get("PORT", 5000))  # Render يعين Port تلقائياً
RETI, RBC = range(2)
user_data = {}

# -------------------------------
# منطق الحساب
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"reti": [], "rbc": []}
    await update.message.reply_text("👋 أهلاً! سنقوم بحساب نسبة الريتيكولوسيت.\n\n"
                                    "أدخل عدد الريتيكولوسيت في Champ 1:")
    return RETI

async def get_reti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = user_data[chat_id]
    try:
        value = int(update.message.text)
        if value < 0:
            raise ValueError
        data["reti"].append(value)
    except ValueError:
        await update.message.reply_text("⚠️ الرجاء إدخال رقم صحيح موجب.")
        return RETI

    if len(data["reti"]) < 10:
        await update.message.reply_text(f"Champ {len(data['reti'])+1}:")
        return RETI
    else:
        await update.message.reply_text("✅ انتهينا من الريتيكولوسيت.\n\n"
                                        "الآن أدخل عدد الكريات الحمراء في ربع Champ 1:")
        return RBC

async def get_rbc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = user_data[chat_id]
    try:
        value = int(update.message.text)
        if value < 0:
            raise ValueError
        data["rbc"].append(value)
    except ValueError:
        await update.message.reply_text("⚠️ الرجاء إدخال رقم صحيح موجب.")
        return RBC

    if len(data["rbc"]) < 3:
        await update.message.reply_text(f"ربع Champ {len(data['rbc'])+1}:")
        return RBC
    else:
        # الحسابات
        reti_total = sum(data["reti"])
        rbc1, rbc2, rbc3 = [v * 4 for v in data["rbc"]]
        avg_rbc = (rbc1 + rbc2 + rbc3) / 3
        rbc_total = avg_rbc * 10
        result =


