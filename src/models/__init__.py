"""
الملف الرئيسي لحزمة النماذج.

يقوم هذا الملف بتجميع وتصدير الكلاسات والوظائف الرئيسية من ملفات النماذج المختلفة
لتسهيل استيرادها في أجزاء أخرى من المشروع.
"""

# استيراد النماذج النصية
from .text_models import BasicTextModel

# استيراد نماذج الصور
from .image_models import BasicImageModel

# استيراد نماذج الصوت
from .audio_models import BasicAudioModel

__all__ = [
    "BasicTextModel",
    "BasicImageModel",
    "BasicAudioModel",
]