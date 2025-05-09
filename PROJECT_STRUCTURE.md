# هيكل مشروع Horus AI Pipeline

هذا الملف يوضح هيكل المشروع وتنظيم الملفات والمجلدات.

## المجلدات الرئيسية

### src/
يحتوي على الكود المصدري الرئيسي للمشروع

- **api/** - واجهة برمجة التطبيقات
  - `api.py` - تعريفات واجهات API
  - `README.md` - وثائق API

- **core/** - المكونات الأساسية للمشروع
  - `app.py` - التطبيق الرئيسي
  - `app_gemini.py` - تكامل مع Gemini
  - `horus_ai_pipeline.py` - خط أنابيب AI الرئيسي
  - `main_pipeline.py` - إعداد خط الأنابيب
  - `orchestrator.py` - تنسيق العمليات

- **models/** - تعريفات النماذج
  - `README.md` - وثائق النماذج

- **utils/** - أدوات مساعدة
  - `config.py` - إعدادات التكوين
  - `gemini_utils.py` - أدوات Gemini
  - `memory_utils.py` - إدارة الذاكرة
  - `vertex_utils.py` - أدوات Vertex AI

### config/
ملفات التكوين
- `pyproject.toml` - إعدادات المشروع

### docker/
ملفات وتكوينات Docker
- `Dockerfile` - ملف Docker الرئيسي للتطوير
- `Dockerfile.test` - ملف Docker لبيئة الاختبار
- `docker-compose.yml` - تكوين Docker Compose
- `.dockerignore` - قائمة الملفات المستثناة
- `README.md` - وثائق Docker

### deploy/
ملفات وأدوات النشر
- `Dockerfile` - ملف Docker للنشر
- `app.yaml` - تكوين App Engine
- `deploy_app_engine.sh` - نصوص نشر App Engine
- `deploy_cloud_run.sh` - نصوص نشر Cloud Run
- `deploy_vertex_endpoint.py` - نشر نقطة نهاية Vertex

### docs/
وثائق المشروع
- `CHANGELOG.md` - سجل التغييرات
- `CONTRIBUTING.md` - دليل المساهمة
- `INDEX.md` - فهرس الوثائق
- **guides/** - أدلة تفصيلية
  - `DEPLOY_GUIDE.md` - دليل النشر
  - `STRATEGY.md` - استراتيجيات المشروع

### tests/
اختبارات المشروع
- **api/** - اختبارات API
- **core/** - اختبارات المكونات الأساسية
- **models/** - اختبارات النماذج
- **utils/** - اختبارات الأدوات المساعدة

### scripts/
نصوص برمجية مساعدة
- `install-dependencies.bat` - تثبيت التبعيات

## الملفات الرئيسية

- `main.py` - نقطة الدخول الرئيسية
- `requirements.txt` - تبعيات المشروع
- `pyproject.toml` - إعدادات بناء المشروع
- `Dockerfile` - تعريف حاوية Docker
- `docker-compose.yml` - تكوين Docker Compose
- `.env.example` - مثال لمتغيرات البيئة
- `LICENSE` - رخصة المشروع
- `README.md` - الوثائق الرئيسية
