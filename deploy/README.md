# أدوات نشر Horus AI Pipeline

<div dir="rtl">

## نظرة عامة

هذا المجلد يحتوي على الأدوات والملفات اللازمة لنشر مشروع Horus AI Pipeline على منصات Google Cloud المختلفة.

## الملفات

- **Dockerfile**: ملف لبناء صورة Docker للمشروع
- **app.yaml**: ملف تكوين App Engine
- **deploy_app_engine.sh**: سكريبت لنشر التطبيق على App Engine
- **deploy_cloud_run.sh**: سكريبت لنشر التطبيق على Cloud Run
- **deploy_vertex_endpoint.py**: سكريبت لنشر نقطة نهاية Vertex AI

## كيفية الاستخدام

### نشر على Cloud Run

```bash
cd deploy
bash deploy_cloud_run.sh
```

### نشر على App Engine

```bash
cd deploy
bash deploy_app_engine.sh
```

### نشر على Vertex AI Endpoint

```bash
cd deploy
python deploy_vertex_endpoint.py
```

## متطلبات النشر

1. تثبيت Google Cloud SDK
2. تكوين gcloud CLI للوصول إلى مشروع Google Cloud الخاص بك
3. تفعيل واجهات برمجة التطبيقات المطلوبة في مشروع Google Cloud
4. تكوين ملف .env بشكل صحيح

## استكشاف الأخطاء وإصلاحها

إذا واجهت مشاكل أثناء النشر، تحقق من:

1. صحة مفتاح JSON وأذونات حساب الخدمة
2. تفعيل واجهات برمجة التطبيقات المطلوبة
3. حدود الاستخدام والكوتا في مشروع Google Cloud الخاص بك

</div>
