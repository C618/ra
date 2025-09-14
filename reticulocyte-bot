from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# مراحل المحادثة
RETI, RBC = range(2)

# تخزين البيانات مؤقتًا
user_data = {}

# دالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"reti": [], "rbc": []}
    await update.message.reply_text("👋 أهلاً! سنقوم بحساب نسبة الريتيكولوسيت.\n\n"
                                    "أدخل عدد الريتيكولوسيت في Champ 1:")
    return RETI

# استقبال قيم الريتيكولوسيت
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

# استقبال قيم الكريات الحمراء
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
        result = (reti_total / rbc_total) * 100

        # عرض النتيجة
        await update.message.reply_text(
            f"--- النتيجة ---\n"
            f"🔹 مجموع الريتيكولوسيت = {reti_total}\n"
            f"🔹 متوسط الكريات الحمراء (×10) = {rbc_total:.2f}\n"
            f"🔹 نسبة الريتيكولوسيت = {result:.2f} %"
        )
        return ConversationHandler.END

# أمر الإلغاء
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 تم إلغاء العملية.")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token("8402125692:AAHndM_lQg6xozZ4WWdu0udgM_BjBmvkV0U").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            RETI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reti)],
            RBC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rbc)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("🤖 البوت شغال ...")
    app.run_polling()


if __name__ == "__main__":
    main()


