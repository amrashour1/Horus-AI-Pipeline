# Dockerfile

FROM python:3.9-slim

WORKDIR /app

# نسخ ملفات المشروع
COPY . .

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1

# تعريض المنفذ 8080 (المنفذ الافتراضي لـ Cloud Run)
EXPOSE 8080

# تشغيل التطبيق
CMD ["python", "horus_ai_pipeline.py"]