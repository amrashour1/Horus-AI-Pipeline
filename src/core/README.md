# وحدات النواة لمشروع Horus AI Pipeline

<div dir="rtl">

## نظرة عامة

هذا المجلد يحتوي على الوحدات الأساسية لمشروع Horus AI Pipeline. هذه الوحدات تشكل العمود الفقري للمشروع وتوفر الوظائف الرئيسية.

## الملفات

- **app.py**: تطبيق Vertex AI الأساسي
- **app_gemini.py**: تطبيق Google AI Studio
- **horus_ai_pipeline.py**: خط الأنابيب الرئيسي
- **main_pipeline.py**: نسخة بديلة من خط الأنابيب


- **orchestrator.py**: منسق العمليات المتعددة

## كيفية الاستخدام

### استخدام app.py (Vertex AI)

```python
from src.core.app import main
main()
```

### استخدام app_gemini.py (Google AI Studio)

```python
from src.core.app_gemini import main
main()
```

### استخدام orchestrator.py

```python
from src.core.orchestrator import main
main()
```

## التطوير

عند تطوير وحدات النواة، يرجى مراعاة:

1. الحفاظ على التوافق مع الوحدات الأخرى
2. كتابة اختبارات شاملة
3. توثيق الواجهات العامة
4. مراعاة الأداء والكفاءة

</div>
