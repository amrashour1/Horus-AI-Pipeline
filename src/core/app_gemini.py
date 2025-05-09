"""
تطبيق Horus AI Pipeline - الجزء الأول (إصدار Google AI Studio)
استخدام نموذج Gemini 1.5 Flash من Google AI Studio
"""

import os
import sys
import logging
from dotenv import load_dotenv

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# استيراد الوحدات المساعدة
from src.utils import gemini_utils, memory_utils

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

# تهيئة الذاكرة
working_memory = memory_utils.init_working_memory()
long_term_memory = memory_utils.init_long_term_memory()
chat_history = []

def initialize_gemini_api():
    """تهيئة Gemini API"""
    return gemini_utils.init_gemini_api()

def get_model():
    """الحصول على نموذج Gemini"""
    return gemini_utils.get_gemini_model(MODEL_NAME)

def process_query(query, model):
    """معالجة استعلام المستخدم"""
    global chat_history

    try:
        # استرجاع السياق من الذاكرة
        context = memory_utils.context_reminder(query, chat_history, long_term_memory, working_memory)

        # إنشاء الاستعلام مع السياق
        prompt = f"""
        السياق: {context}

        استعلام المستخدم: {query}

        قم بالإجابة على استعلام المستخدم بناءً على السياق المتوفر.
        """

        # استدعاء النموذج
        response = gemini_utils.call_gemini_direct(model, prompt)

        # تحديث الذاكرة والتاريخ
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})

        # حفظ في الذاكرة طويلة المدى
        long_term_memory.add([query, response])

        return response
    except Exception as e:
        logger.error(f"خطأ في معالجة الاستعلام: {str(e)}")
        return f"عذراً، حدث خطأ أثناء معالجة استعلامك: {str(e)}"

def main():
    """الدالة الرئيسية للتطبيق"""
    print("=== نظام Horus AI Pipeline - الجزء الأول (إصدار Google AI Studio) ===")

    # تهيئة Gemini API
    if not initialize_gemini_api():
        print("فشل في تهيئة Gemini API. يرجى التحقق من مفتاح API والاتصال.")
        return

    # تحميل النموذج
    model = get_model()
    if not model:
        print("فشل في تحميل النموذج. يرجى التحقق من اسم النموذج والاتصال.")
        return

    print(f"تم تهيئة النظام بنجاح! يستخدم نموذج {MODEL_NAME}")
    print("أدخل 'خروج' للخروج من البرنامج")

    # حلقة المحادثة
    while True:
        query = input("\nاستعلامك: ")
        if query.lower() in ['خروج', 'exit', 'quit']:
            break

        response = process_query(query, model)
        print(f"\nالرد: {response}")

    print("شكراً لاستخدام نظام Horus AI Pipeline!")

if __name__ == "__main__":
    main()
