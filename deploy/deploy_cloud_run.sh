#!/bin/bash

# سكريبت لنشر التطبيق على Google Cloud Run

# تعيين متغيرات
PROJECT_ID="horus-ai-pipeline"
REGION="us-central1"
SERVICE_NAME="horus-ai"

# تأكيد المتغيرات
echo "سيتم نشر التطبيق باستخدام المعلومات التالية:"
echo "معرف المشروع: $PROJECT_ID"
echo "المنطقة: $REGION"
echo "اسم الخدمة: $SERVICE_NAME"
echo ""
read -p "هل تريد المتابعة؟ (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "تم إلغاء النشر."
    exit 1
fi

# بناء صورة Docker ودفعها إلى Container Registry
echo "جاري بناء صورة Docker..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# نشر الخدمة على Cloud Run
echo "جاري نشر الخدمة على Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated

echo "تم نشر التطبيق بنجاح!"
