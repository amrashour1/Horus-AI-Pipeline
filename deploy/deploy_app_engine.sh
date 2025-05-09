#!/bin/bash

# سكريبت لنشر التطبيق على Google App Engine

# تعيين متغيرات
PROJECT_ID="horus-ai-pipeline"
REGION="us-central1"

# تأكيد المتغيرات
echo "سيتم نشر التطبيق على App Engine باستخدام المعلومات التالية:"
echo "معرف المشروع: $PROJECT_ID"
echo "المنطقة: $REGION"
echo ""
read -p "هل تريد المتابعة؟ (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "تم إلغاء النشر."
    exit 1
fi

# تحديث معرف المشروع في ملف app.yaml
sed -i "s/PROJECT_ID: \".*\"/PROJECT_ID: \"$PROJECT_ID\"/" app.yaml
sed -i "s/REGION: \".*\"/REGION: \"$REGION\"/" app.yaml

# نشر التطبيق على App Engine
echo "جاري نشر التطبيق على App Engine..."
gcloud app deploy --project=$PROJECT_ID

echo "تم نشر التطبيق بنجاح!"
