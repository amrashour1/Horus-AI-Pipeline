# دليل نشر مشروع Horus AI Pipeline على Google Cloud

<div dir="rtl">

## مقدمة

هذا الدليل يوضح خطوات نشر مشروع Horus AI Pipeline على منصة Google Cloud. المشروع مصمم للعمل مع Vertex AI وGemini 2.5 Flash، ويمكن نشره باستخدام إحدى الطرق التالية:

1. **Google Cloud Run**: مناسب للتطبيقات الحديثة المعتمدة على الحاويات (Containers) وتتميز بالتدرج التلقائي.
2. **Google App Engine**: مناسب للتطبيقات التقليدية وتوفر بيئة مُدارة بالكامل.

## المتطلبات الأساسية

- حساب Google Cloud Platform مع مشروع نشط
- تثبيت Google Cloud SDK على جهازك المحلي
- تفعيل فوترة المشروع على Google Cloud
- تفعيل واجهات برمجة التطبيقات (APIs) المطلوبة

## الخطوة 1: إعداد البيئة المحلية

### تثبيت Google Cloud SDK

1. قم بتنزيل وتثبيت [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. قم بتسجيل الدخول باستخدام الأمر:
   ```bash
   gcloud auth login
   ```
3. قم بتعيين المشروع الافتراضي:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

### إعداد ملف البيئة

1. قم بنسخ ملف `.env.example` إلى `.env`:
   ```bash
   cp .env.example .env
   ```

2. قم بتعديل ملف `.env` بالقيم الصحيحة:
   ```
   PROJECT_ID=your-project-id
   REGION=us-central1
   KEY_PATH=path/to/your-key.json
   REDIS_HOST=your-redis-host
   ```

### إنشاء مفتاح حساب الخدمة

1. انتقل إلى [صفحة حسابات الخدمة](https://console.cloud.google.com/iam-admin/serviceaccounts) في مشروع Google Cloud الخاص بك
2. انقر على "إنشاء حساب خدمة"
3. أدخل اسمًا ووصفًا لحساب الخدمة
4. امنح الأدوار التالية لحساب الخدمة:
   - `roles/aiplatform.user`
   - `roles/storage.admin`
5. انقر على "إنشاء مفتاح" واختر نوع المفتاح JSON
6. احفظ ملف المفتاح في مكان آمن وقم بتحديث مسار الملف في `.env`

### تفعيل واجهات برمجة التطبيقات المطلوبة

```bash
gcloud services enable aiplatform.googleapis.com storage.googleapis.com iam.googleapis.com run.googleapis.com appengine.googleapis.com
```

## الخطوة 2: تحضير المشروع للنشر

### تعديل ملف Dockerfile (لـ Cloud Run)

تأكد من أن ملف `Dockerfile` يحتوي على التكوين الصحيح:

```dockerfile
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
```

### تعديل ملف app.yaml (لـ App Engine)

تأكد من أن ملف `app.yaml` يحتوي على التكوين الصحيح:

```yaml
runtime: python39
entrypoint: python horus_ai_pipeline.py

env_variables:
  PROJECT_ID: "your-project-id"
  REGION: "us-central1"

# تكوين مثيل الخادم
instance_class: F2

# تكوين التدرج التلقائي
automatic_scaling:
  min_instances: 1
  max_instances: 5
  target_cpu_utilization: 0.65

# تكوين الذاكرة والوحدة المركزية
resources:
  cpu: 1
  memory_gb: 2
  disk_size_gb: 10
```

## الخطوة 3: إعداد خدمات الذاكرة

### إعداد Redis (للذاكرة العاملة)

1. إنشاء مثيل Redis على Google Cloud Memorystore:
   ```bash
   gcloud redis instances create horus-memory \
     --size=1 \
     --region=us-central1 \
     --redis-version=redis_6_x
   ```

2. الحصول على عنوان IP الخاص بمثيل Redis:
   ```bash
   gcloud redis instances describe horus-memory --region=us-central1
   ```

3. تحديث متغير `REDIS_HOST` في ملف `.env` بعنوان IP الذي حصلت عليه

## الخطوة 4: نشر المشروع

### الخيار 1: النشر على Cloud Run

1. بناء صورة Docker ودفعها إلى Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/horus-ai
   ```

2. نشر الصورة على Cloud Run:
   ```bash
   gcloud run deploy horus-ai \
     --image gcr.io/YOUR_PROJECT_ID/horus-ai \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --set-env-vars PROJECT_ID=YOUR_PROJECT_ID,REGION=us-central1,REDIS_HOST=YOUR_REDIS_IP
   ```

3. إضافة مفتاح حساب الخدمة كسر (Secret) في Cloud Run:
   ```bash
   # إنشاء السر
   gcloud secrets create horus-key --data-file=path/to/your-key.json
   
   # منح الوصول للخدمة
   gcloud secrets add-iam-policy-binding horus-key \
     --member=serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor
   
   # تحديث الخدمة لاستخدام السر
   gcloud run services update horus-ai \
     --update-secrets=KEY_PATH=/horus-key:latest
   ```

### الخيار 2: النشر على App Engine

1. تأكد من تحديث متغيرات البيئة في ملف `app.yaml`

2. نشر التطبيق على App Engine:
   ```bash
   gcloud app deploy
   ```

3. عرض التطبيق المنشور:
   ```bash
   gcloud app browse
   ```

## الخطوة 5: التحقق من النشر

### التحقق من سجلات التطبيق

#### لـ Cloud Run:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=horus-ai" --limit=10
```

#### لـ App Engine:
```bash
gcloud app logs read --limit=10
```

### اختبار التطبيق

1. الحصول على عنوان URL للتطبيق المنشور:
   - لـ Cloud Run: `gcloud run services describe horus-ai --format="value(status.url)"`
   - لـ App Engine: `gcloud app describe --format="value(defaultHostname)"`

2. إرسال طلب اختبار إلى التطبيق باستخدام curl أو أي أداة أخرى

## الخطوة 6: إعداد التدرج التلقائي والمراقبة

### إعداد التنبيهات

1. انتقل إلى [Cloud Monitoring](https://console.cloud.google.com/monitoring)
2. قم بإنشاء لوحة معلومات مخصصة لمراقبة أداء التطبيق
3. قم بإعداد تنبيهات للمقاييس الهامة مثل استخدام وحدة المعالجة المركزية والذاكرة وزمن الاستجابة

### إعداد النسخ الاحتياطي

1. قم بإعداد نسخ احتياطي دوري لبيانات Redis:
   ```bash
   gcloud scheduler jobs create http redis-backup \
     --schedule="0 0 * * *" \
     --uri="https://YOUR_BACKUP_ENDPOINT" \
     --http-method=POST
   ```

## استكشاف الأخطاء وإصلاحها

### مشاكل شائعة وحلولها

1. **خطأ في الاتصال بـ Vertex AI**:
   - تأكد من تفعيل واجهة برمجة التطبيقات `aiplatform.googleapis.com`
   - تحقق من صلاحيات حساب الخدمة

2. **خطأ في الاتصال بـ Redis**:
   - تأكد من إعداد شبكة VPC الصحيحة للوصول إلى Redis
   - تحقق من عنوان IP الصحيح لـ Redis في متغيرات البيئة

3. **مشاكل في نشر الصورة على Cloud Run**:
   - تحقق من سجلات البناء: `gcloud builds list`
   - تحقق من سجلات Cloud Run: `gcloud logging read "resource.type=cloud_run_revision"`

## الموارد الإضافية

- [وثائق Google Cloud Run](https://cloud.google.com/run/docs)
- [وثائق Google App Engine](https://cloud.google.com/appengine/docs)
- [وثائق Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [وثائق Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis)

</div>