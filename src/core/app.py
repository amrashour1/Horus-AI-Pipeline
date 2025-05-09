"""
تطبيق Horus AI Pipeline - الجزء الأول
استخدام نموذج Gemini 1.5 Flash من Google Cloud
"""

import os
import sys
import logging
from dotenv import load_dotenv

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# استيراد الوحدات المساعدة
from src.utils import vertex_utils, memory_utils

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
KEY_PATH = os.getenv("KEY_PATH")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

# تهيئة الذاكرة
working_memory = memory_utils.init_working_memory()
long_term_memory = memory_utils.init_long_term_memory()
chat_history = []

def initialize_vertex_ai():
    """تهيئة Vertex AI"""
    try:
        vertex_utils.init_vertex(PROJECT_ID, REGION, KEY_PATH)
        logger.info(f"تم تهيئة Vertex AI بنجاح. المشروع: {PROJECT_ID}, المنطقة: {REGION}")
        return True
    except Exception as e:
        logger.error(f"خطأ في تهيئة Vertex AI: {str(e)}")
        return False

def get_model():
    """الحصول على نموذج Gemini"""
    try:
        model = vertex_utils.get_gemini_model(MODEL_NAME)
        logger.info(f"تم تحميل النموذج {MODEL_NAME} بنجاح")
        return model
    except Exception as e:
        logger.error(f"خطأ في تحميل النموذج: {str(e)}")
        return None

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
        response = vertex_utils.call_gemini_direct(model, prompt)

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
    print("=== نظام Horus AI Pipeline - الجزء الأول ===")

    # تهيئة Vertex AI
    if not initialize_vertex_ai():
        print("فشل في تهيئة Vertex AI. يرجى التحقق من متغيرات البيئة والاتصال.")
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
