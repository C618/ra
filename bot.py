import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from uuid import uuid4

# تكوين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# استبدل هذا بـ API token الخاص ببوتك
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI')

# مجلد لتخزين الفيديوهات مؤقتاً
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler لأمر /start"""
    await update.message.reply_text(
        "مرحباً! أنا بوت تحميل الفيديو. أرسل لي أي فيديو وسأقوم بتنزيله وتخزينه.\n\n"
        "يمكنك استخدام الأمر /download لتحميل فيديو من رابط أيضًا."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler لتحميل فيديو من رابط"""
    if not context.args:
        await update.message.reply_text("يرجى إرسال رابط الفيديو بعد الأمر /download")
        return
    
    url = context.args[0]
    try:
        await update.message.reply_text("جاري تحميل الفيديو، يرجى الانتظار...")
        
        # إنشاء اسم فريد للملف
        file_name = f"{uuid4().hex}.mp4"
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        
        # تحميل الفيديو من الرابط
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # إرسال الفيديو للمستخدم
            await update.message.reply_video(
                video=open(file_path, 'rb'),
                caption="تم تحميل الفيديو بنجاح!"
            )
            
            # تنظيف الملف المؤقت
            os.remove(file_path)
        else:
            await update.message.reply_text("فشل في تحميل الفيديو من الرابط الم provided.")
            
    except Exception as e:
        logger.error(f"Error downloading video from URL: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة الفيديو.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الفيديوهات المرسلة"""
    try:
        # الحصول على ملف الفيديو
        video_file = await update.message.video.get_file()
        
        # إنشاء اسم فريد للملف
        file_name = f"{uuid4().hex}.mp4"
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        
        # تنزيل الفيديو
        await video_file.download_to_drive(file_path)
        
        # إرسال رسالة تأكيد
        await update.message.reply_text(
            f"تم تنزيل الفيديو بنجاح!\n"
            f"اسم الملف: {file_name}\n"
            f"الحجم: {os.path.getsize(file_path)} بايت\n\n"
            f"يمكنك الآن مشاركته مع الآخرين."
        )
        
        # (اختياري) حذف الملف بعد التخزين إذا كنت تريد توفير المساحة
        # os.remove(file_path)
        
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة الفيديو.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأخطاء"""
    logger.error(f"حدث خطأ: {context.error}")

def main():
    # إنشاء التطبيق
    application = Application.builder().token(API_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download_video))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_error_handler(error_handler)
    
    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()