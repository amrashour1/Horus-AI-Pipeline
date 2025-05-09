# أدوات مساعدة لمشروع Horus AI Pipeline

<div dir="rtl">

## نظرة عامة

هذا المجلد يحتوي على الأدوات المساعدة والوظائف المشتركة لمشروع Horus AI Pipeline. هذه الأدوات تستخدم في مختلف أجزاء المشروع لتوفير وظائف مشتركة.

## الملفات

- **vertex_utils.py**: أدوات للتفاعل مع Vertex AI
- **gemini_utils.py**: أدوات للتفاعل مع Google AI Studio
- **memory_utils.py**: أدوات إدارة الذاكرة
- **config.py**: إعدادات التكوين

## كيفية الاستخدام

### استخدام vertex_utils.py

```python
from src.utils.vertex_utils import init_vertex, get_gemini_model, call_gemini_direct

# تهيئة Vertex AI
init_vertex(project_id, region, credentials_path)

# الحصول على نموذج Gemini
model = get_gemini_model(model_name)

# استدعاء النموذج
response = call_gemini_direct(model, prompt)
```

### استخدام gemini_utils.py

```python
from src.utils.gemini_utils import init_gemini_api, get_gemini_model, call_gemini_direct

# تهيئة Gemini API
init_gemini_api()

# الحصول على نموذج Gemini
model = get_gemini_model(model_name)

# استدعاء النموذج
response = call_gemini_direct(model, prompt)
```

### استخدام memory_utils.py

```python
from src.utils.memory_utils import init_working_memory, init_long_term_memory, context_reminder

# تهيئة الذاكرة
working_memory = init_working_memory()
long_term_memory = init_long_term_memory()

# استرجاع السياق
context = context_reminder(query, chat_history, long_term_memory, working_memory)
```

## التطوير

عند تطوير الأدوات المساعدة، يرجى مراعاة:

1. إعادة استخدام الكود قدر الإمكان
2. توفير واجهات متسقة
3. معالجة الأخطاء بشكل مناسب
4. توثيق الوظائف بشكل جيد

</div>
