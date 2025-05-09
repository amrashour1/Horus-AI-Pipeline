# مشروع Horus AI Pipeline

<div dir="rtl">

## نظرة عامة

مشروع Horus AI Pipeline هو منصة متكاملة لمعالجة اللغة الطبيعية باستخدام نماذج Google AI المتقدمة. يوفر المشروع واجهات متعددة للتفاعل مع نماذج الذكاء الاصطناعي، بما في ذلك Vertex AI وGoogle AI Studio.

## المميزات الرئيسية

- دعم نماذج Gemini 1.5 Flash من Google Cloud
- واجهة سطر أوامر بسيطة للتفاعل مع النماذج
- واجهة برمجة تطبيقات (API) للتكامل مع التطبيقات الأخرى
- نظام ذاكرة لتخزين واسترجاع المحادثات السابقة
- أدوات نشر متعددة لمنصات Google Cloud المختلفة

## هيكل المشروع

تم تنظيم المشروع بطريقة منهجية لتسهيل التطوير والصيانة. للحصول على تفاصيل كاملة عن هيكل المشروع، يرجى الاطلاع على ملف [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

فيما يلي نظرة عامة على الهيكل الجديد للمشروع:

### المجلدات الرئيسية

- **src/**: المصدر الرئيسي للكود
  - **core/**: الوحدات الأساسية للمشروع
  - **utils/**: أدوات مساعدة ووظائف مشتركة
  - **api/**: واجهة برمجة التطبيقات
  - **models/**: تعريفات النماذج والهياكل البيانية
- **tests/**: جميع ملفات الاختبار
  - **core/**: اختبارات الوحدات الأساسية
  - **utils/**: اختبارات الأدوات المساعدة
  - **api/**: اختبارات واجهة البرمجة
- **docs/readmes/**: جميع ملفات README

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

#### اختبارات الأدوات المساعدة (tests/utils/)
- **test_vertex_utils.py**: اختبارات أدوات Vertex AI
- **test_gemini_utils.py**: اختبارات أدوات Google AI Studio
- **test_memory_utils.py**: اختبارات نظام الذاكرة

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

#### الوثائق (docs/)
- **README.md**: الوثيقة الرئيسية للمشروع
- **guides/DEPLOY_GUIDE.md**: دليل النشر
- **guides/STRATEGY.md**: استراتيجية المشروع

## كيفية الاستخدام

### تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### تكوين المشروع

1. قم بنسخ ملف `.env.example` إلى `.env`
2. قم بتعديل ملف `.env` لإضافة معلومات مشروع Google Cloud الخاص بك
3. قم بتشغيل سكريبت الإعداد:

```bash
python setup.py
```

### تشغيل المشروع

#### باستخدام Python مباشرة

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

#### باستخدام Docker

يمكنك تشغيل المشروع باستخدام Docker بسهولة:

```bash
# في نظام Linux/macOS
./start-horus.sh

# في نظام Windows (CMD)
start-horus.bat

# في نظام Windows (PowerShell)
.\start-horus.ps1
```

لإعادة بناء التطبيق:

```bash
# في نظام Linux/macOS
./start-horus.sh --build

# في نظام Windows (CMD)
start-horus.bat --build

# في نظام Windows (PowerShell)
.\start-horus.ps1 -Build
```

لإيقاف التطبيق:

```bash
# في نظام Linux/macOS
./start-horus.sh --stop

# في نظام Windows (CMD)
start-horus.bat --stop

# في نظام Windows (PowerShell)
.\start-horus.ps1 -Stop
```

بعد تشغيل التطبيق، يمكنك الوصول إليه على العنوان التالي:
[http://localhost:8080](http://localhost:8080)

للحصول على تفاصيل كاملة حول استخدام Docker مع المشروع، يرجى الاطلاع على [دليل Docker](DOCKER_README.md).

### تشغيل الاختبارات

```bash
pytest
```

## المساهمة في المشروع

للمساهمة في المشروع، يرجى الاطلاع على [دليل المساهمة](docs/CONTRIBUTING.md).

## الترخيص

هذا المشروع مرخص بموجب [رخصة MIT](LICENSE).

## المزيد من المعلومات

للحصول على معلومات تفصيلية حول كيفية استخدام المشروع، يرجى الاطلاع على الوثائق في مجلد `docs/`.

</div>
