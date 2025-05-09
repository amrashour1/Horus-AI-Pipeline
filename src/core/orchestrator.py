"""
Horus AI Pipeline - الجزء الثاني
نظام متكامل متعدد النماذج مع ذاكرة متقدمة
"""

import os
import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
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

# تكوين النماذج
MODELS = {
    "fast": os.getenv("FAST_MODEL", "gemini-1.5-flash"),
    "analysis": os.getenv("ANALYSIS_MODEL", "gemini-1.5-pro"),
    "deep_thinking": os.getenv("DEEP_MODEL", "gemini-1.5-pro"),
    "summary": os.getenv("SUMMARY_MODEL", "gemini-1.5-flash")
}

# تهيئة الذاكرة
working_memory = None
long_term_memory = None
chat_history = []

def initialize_system():
    """تهيئة النظام بالكامل"""
    global working_memory, long_term_memory

    # تهيئة Vertex AI
    try:
        vertex_utils.init_vertex(PROJECT_ID, REGION, KEY_PATH)
        logger.info(f"تم تهيئة Vertex AI بنجاح. المشروع: {PROJECT_ID}, المنطقة: {REGION}")
    except Exception as e:
        logger.error(f"خطأ في تهيئة Vertex AI: {str(e)}")
        return False

    # تهيئة الذاكرة
    try:
        working_memory = memory_utils.init_working_memory()
        long_term_memory = memory_utils.init_long_term_memory()
        logger.info("تم تهيئة أنظمة الذاكرة بنجاح")
    except Exception as e:
        logger.error(f"خطأ في تهيئة الذاكرة: {str(e)}")
        return False

    # تحميل النماذج
    try:
        for model_type, model_name in MODELS.items():
            logger.info(f"جاري تحميل نموذج {model_type}: {model_name}")
            # في المرحلة الثانية، يمكن تحميل النماذج مسبقًا أو عند الطلب
    except Exception as e:
        logger.error(f"خطأ في تحميل النماذج: {str(e)}")
        return False

    return True

def get_model(model_type):
    """الحصول على نموذج محدد"""
    model_name = MODELS.get(model_type)
    if not model_name:
        logger.warning(f"نوع النموذج غير معروف: {model_type}. استخدام النموذج السريع بدلاً من ذلك.")
        model_name = MODELS["fast"]

    try:
        model = vertex_utils.get_gemini_model(model_name)
        return model
    except Exception as e:
        logger.error(f"خطأ في تحميل النموذج {model_name}: {str(e)}")
        return None

def fast_analysis(query, context):
    """تحليل سريع باستخدام النموذج السريع"""
    model = get_model("fast")
    if not model:
        return "غير قادر على إجراء تحليل سريع بسبب خطأ في تحميل النموذج."

    prompt = f"""
    السياق: {context}

    قم بإجراء تحليل سريع للاستعلام التالي:
    {query}

    أعط إجابة موجزة ومباشرة.
    """

    try:
        return vertex_utils.call_gemini_direct(model, prompt)
    except Exception as e:
        logger.error(f"خطأ في التحليل السريع: {str(e)}")
        return f"خطأ في التحليل السريع: {str(e)}"

def deep_analysis(query, context):
    """تحليل عميق باستخدام النموذج التحليلي"""
    model = get_model("analysis")
    if not model:
        return "غير قادر على إجراء تحليل عميق بسبب خطأ في تحميل النموذج."

    prompt = f"""
    السياق: {context}

    قم بإجراء تحليل عميق ومفصل للاستعلام التالي:
    {query}

    فكر خطوة بخطوة وقدم تحليلاً شاملاً.
    """

    try:
        return vertex_utils.call_gemini_direct(model, prompt)
    except Exception as e:
        logger.error(f"خطأ في التحليل العميق: {str(e)}")
        return f"خطأ في التحليل العميق: {str(e)}"

def logical_reasoning(query, context):
    """استدلال منطقي باستخدام نموذج التفكير العميق"""
    model = get_model("deep_thinking")
    if not model:
        return "غير قادر على إجراء استدلال منطقي بسبب خطأ في تحميل النموذج."

    prompt = f"""
    السياق: {context}

    قم بإجراء استدلال منطقي للاستعلام التالي:
    {query}

    فكر بشكل منطقي ومنهجي، وقدم استنتاجات مدعومة بالأدلة.
    """

    try:
        return vertex_utils.call_gemini_direct(model, prompt)
    except Exception as e:
        logger.error(f"خطأ في الاستدلال المنطقي: {str(e)}")
        return f"خطأ في الاستدلال المنطقي: {str(e)}"

def summarize_results(query, results, context):
    """تلخيص النتائج باستخدام نموذج التلخيص"""
    model = get_model("summary")
    if not model:
        return "غير قادر على تلخيص النتائج بسبب خطأ في تحميل النموذج."

    prompt = f"""
    السياق: {context}

    الاستعلام الأصلي: {query}

    نتائج التحليلات:
    1. تحليل سريع: {results.get('fast', 'غير متوفر')}
    2. تحليل عميق: {results.get('deep', 'غير متوفر')}
    3. استدلال منطقي: {results.get('logical', 'غير متوفر')}

    قم بتلخيص هذه النتائج في إجابة متماسكة وشاملة. ركز على النقاط الأكثر أهمية وقدم إجابة نهائية للاستعلام الأصلي.
    """

    try:
        return vertex_utils.call_gemini_direct(model, prompt)
    except Exception as e:
        logger.error(f"خطأ في تلخيص النتائج: {str(e)}")
        return f"خطأ في تلخيص النتائج: {str(e)}"

def process_query(query):
    """معالجة استعلام المستخدم باستخدام النظام المتكامل"""
    global chat_history

    # استرجاع السياق من الذاكرة
    context = memory_utils.context_reminder(query, chat_history, long_term_memory, working_memory)

    # تنفيذ التحليلات المتوازية
    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        fast_future = executor.submit(fast_analysis, query, context)
        deep_future = executor.submit(deep_analysis, query, context)
        logical_future = executor.submit(logical_reasoning, query, context)

        results["fast"] = fast_future.result()
        results["deep"] = deep_future.result()
        results["logical"] = logical_future.result()

    # تلخيص النتائج
    final_response = summarize_results(query, results, context)

    # تحديث الذاكرة والتاريخ
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": final_response})

    # حفظ في الذاكرة طويلة المدى
    long_term_memory.add([query, final_response])

    return final_response

def main():
    """الدالة الرئيسية للتطبيق"""
    print("=== نظام Horus AI Pipeline - الجزء الثاني (متعدد النماذج) ===")

    # تهيئة النظام
    if not initialize_system():
        print("فشل في تهيئة النظام. يرجى التحقق من السجلات للحصول على مزيد من المعلومات.")
        return

    print("تم تهيئة النظام بنجاح!")
    print("أدخل 'خروج' للخروج من البرنامج")

    # حلقة المحادثة
    while True:
        query = input("\nاستعلامك: ")
        if query.lower() in ['خروج', 'exit', 'quit']:
            break

        print("\nجاري معالجة استعلامك (قد يستغرق هذا بضع ثوانٍ)...")
        response = process_query(query)
        print(f"\nالرد: {response}")

    print("شكراً لاستخدام نظام Horus AI Pipeline!")

if __name__ == "__main__":
    main()
