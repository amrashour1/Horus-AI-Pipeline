# Dockerfile

# مرحلة البناء
FROM python:3.9-slim as builder

WORKDIR /app

# تثبيت الأدوات المطلوبة للبناء
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# نسخ ملف المتطلبات
COPY requirements.txt .

# إنشاء بيئة افتراضية
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# مرحلة التشغيل
FROM python:3.9-slim

WORKDIR /app

# نسخ البيئة الافتراضية من مرحلة البناء
COPY --from=builder /opt/venv /opt/venv

# نسخ ملفات التطبيق
COPY . .

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PROJECT_ID=rock-atlas-451404-c0
ENV REGION=us-central1
ENV MODEL_NAME=gemini-1.5-flash
ENV PORT=8080
ENV PYTHONPATH=/app

# تعريض المنفذ
EXPOSE 8080

# تثبيت curl لفحص الصحة
RUN apt-get update && apt-get install -y curl

# تشغيل التطبيق
CMD ["python", "horus_ai_core.py"]