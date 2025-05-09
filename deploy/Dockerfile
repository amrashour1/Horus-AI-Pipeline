# Dockerfile

FROM python:3.9-slim

WORKDIR /app

# تثبيت المكتبات الأساسية
RUN pip install --no-cache-dir --upgrade pip

# نسخ ملف المتطلبات أولاً لتحسين التخزين المؤقت
COPY requirements.txt .

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# نسخ بقية ملفات المشروع
COPY . .

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PROJECT_ID=rock-atlas-451404-c0
ENV REGION=us-central1
ENV MODEL_NAME=gemini-1.5-flash
ENV PORT=8080
ENV PYTHONPATH=/app

# تعريض المنفذ 8080 (المنفذ الافتراضي لـ Cloud Run)
EXPOSE 8080

# تشغيل التطبيق
CMD ["python", "main.py", "--mode", "api"]