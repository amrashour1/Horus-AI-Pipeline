# اختبارات Horus AI Pipeline

هذا المجلد يحتوي على اختبارات لمشروع Horus AI Pipeline.

## بنية المجلد

```
tests/
├── api/                  # اختبارات لوحدات API
├── core/                 # اختبارات لوحدات Core
├── test_api/             # اختبارات إضافية لوحدات API
├── test_core/            # اختبارات إضافية لوحدات Core
├── test_models/          # اختبارات للنماذج
├── test_utils/           # اختبارات للأدوات المساعدة
├── utils/                # أدوات مساعدة للاختبارات
├── conftest.py           # تكوين pytest
├── README.md             # ملف الشرح الرئيسي
├── test_main.py          # اختبارات للملف الرئيسي
├── test_run.py           # اختبارات للتشغيل
├── __init__.py           # ملف تعريف الحزمة
├── test_api.py           # تطبيق API بسيط للاختبار
├── test_dependencies.py  # اختبار للتحقق من تثبيت المكتبات
├── check_dependencies.bat # سكريبت للتحقق من تثبيت المكتبات
├── install_dependencies.bat # سكريبت لتثبيت المكتبات
├── run_api_tests.bat     # سكريبت لتشغيل اختبارات API
└── run_test_api.bat      # سكريبت لتشغيل تطبيق API للاختبار
```

## كيفية تشغيل الاختبارات

### 1. التحقق من تثبيت المكتبات

```
.\check_dependencies.bat
```

### 2. تثبيت المكتبات المطلوبة

```
.\install_dependencies.bat
```

### 3. تشغيل اختبارات API

```
.\run_api_tests.bat
```

### 4. تشغيل تطبيق API للاختبار

```
.\run_test_api.bat
```

## إضافة اختبارات جديدة

لإضافة اختبارات جديدة، قم بإنشاء ملف جديد في المجلد المناسب واتبع نمط الاختبارات الموجودة.

مثال:

```python
def test_new_feature():
    # اختبار للميزة الجديدة
    assert True
```
