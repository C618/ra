FROM python:3.11-slim

WORKDIR /app

# نسخ الملفات
COPY requirements.txt .
COPY bot.py .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل البوت
CMD ["python", "bot.py"]
