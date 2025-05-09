# اختبارات مشروع Horus AI Pipeline

<div dir="rtl">

## نظرة عامة

هذا المجلد يحتوي على اختبارات مشروع Horus AI Pipeline. الاختبارات مهمة للتأكد من أن المشروع يعمل بشكل صحيح وأن التغييرات الجديدة لا تكسر الوظائف الحالية.

## هيكل الاختبارات

- **test_utils/**: اختبارات الأدوات المساعدة
- **test_core/**: اختبارات وحدات النواة
- **test_api/**: اختبارات واجهة برمجة التطبيقات
- **test_models/**: اختبارات النماذج

## كيفية تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات محددة
pytest tests/test_utils/

# تشغيل اختبار محدد
pytest tests/test_utils/test_memory_utils.py

# تشغيل دالة اختبار محددة
pytest tests/test_utils/test_memory_utils.py::test_init_working_memory
```

## كتابة اختبارات جديدة

عند كتابة اختبارات جديدة، يرجى اتباع المبادئ التالية:

1. استخدام pytest كإطار عمل للاختبارات
2. كتابة اختبارات وحدة صغيرة ومركزة
3. استخدام fixtures لإعداد بيئة الاختبار
4. استخدام mocks لعزل الوحدة المختبرة

## مثال على اختبار

```python
import pytest
from src.utils.memory_utils import init_working_memory

def test_init_working_memory():
    # إعداد
    memory = init_working_memory()
    
    # تنفيذ
    result = memory.get("test_key", default="default_value")
    
    # تحقق
    assert result == "default_value"
    
    # تنفيذ
    memory.set("test_key", "test_value")
    result = memory.get("test_key")
    
    # تحقق
    assert result == "test_value"
```

</div>
