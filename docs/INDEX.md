# فهرس وثائق مشروع Horus AI Pipeline

<div dir="rtl">

## الوثائق الرئيسية

- [دليل المستخدم الرئيسي](README.md) - نظرة عامة على المشروع وكيفية استخدامه
- [خطة المشروع](PROJECT_PLAN.md) - خطة المشروع التفصيلية والميزانية والجدول الزمني والنماذج المستخدمة

## أدلة متخصصة

- [دليل النشر](guides/DEPLOY_GUIDE.md) - تعليمات مفصلة لنشر المشروع على Google Cloud
- [استراتيجية المشروع](guides/STRATEGY.md) - استراتيجية تطوير وتنفيذ المشروع

## هيكل المشروع

### المجلدات الرئيسية

- **src/**: المصدر الرئيسي للكود
  - **core/**: الوحدات الأساسية للمشروع
  - **utils/**: أدوات مساعدة ووظائف مشتركة
  - **api/**: واجهة برمجة التطبيقات
  - **models/**: تعريفات النماذج والهياكل البيانية

- **docs/**: الوثائق
  - **guides/**: أدلة تفصيلية للاستخدام والنشر

- **deploy/**: ملفات وأدوات النشر

### الملفات الرئيسية

#### وحدات النواة (src/core/)
- **app.py**: تطبيق Vertex AI الأساسي
- **app_gemini.py**: تطبيق Google AI Studio
- **horus_ai_pipeline.py**: خط الأنابيب الرئيسي
- **main_pipeline.py**: نسخة بديلة من خط الأنابيب
- **orchestrator.py**: منسق العمليات المتعددة

#### الأدوات المساعدة (src/utils/)
- **vertex_utils.py**: أدوات للتفاعل مع Vertex AI
- **gemini_utils.py**: أدوات للتفاعل مع Google AI Studio
- **memory_utils.py**: أدوات إدارة الذاكرة
- **config.py**: إعدادات التكوين

#### واجهة برمجة التطبيقات (src/api/)
- **api.py**: واجهة برمجة التطبيقات الرئيسية

#### أدوات النشر (deploy/)
- **Dockerfile**: ملف لبناء صورة Docker
- **app.yaml**: ملف تكوين App Engine
- **deploy_app_engine.sh**: سكريبت لنشر التطبيق على App Engine
- **deploy_cloud_run.sh**: سكريبت لنشر التطبيق على Cloud Run
- **deploy_vertex_endpoint.py**: سكريبت لنشر نقطة نهاية Vertex AI

## كيفية تشغيل المشروع

### باستخدام الملف الرئيسي

```bash
# تشغيل باستخدام Google AI Studio (الافتراضي)
python main.py

# تشغيل باستخدام Vertex AI
python main.py --mode vertex

# تشغيل واجهة برمجة التطبيقات
python main.py --mode api

# تشغيل المنسق
python main.py --mode orchestrator
```

### تشغيل الوحدات مباشرة

```bash
# تشغيل باستخدام Google AI Studio
python src/core/app_gemini.py

# تشغيل باستخدام Vertex AI
python src/core/app.py

# تشغيل واجهة برمجة التطبيقات
python src/api/api.py

# تشغيل المنسق
python src/core/orchestrator.py
```

</div>
