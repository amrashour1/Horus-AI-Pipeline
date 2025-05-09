# horus_ai_pipeline.py

# تطبيق ذكاء اصطناعي متكامل باستخدام Google Cloud Vertex AI وGemini
# للتهيئة والإعداد، قم بتنفيذ: python setup.py
# للنشر على Google Cloud، قم بتنفيذ: python setup.py --deploy run

from vertex_utils import init_vertex, deploy_model, call_gemini
from memory_utils import init_working_memory, init_long_term_memory, context_reminder
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import logging
from config import PROJECT_ID, REGION, KEY_PATH, REDIS_HOST, IMAGE_URI, validate_config

# ----- إعداد التسجيل ----- 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ----- التحقق من صحة الإعدادات ----- 
def initialize_services():
    if not validate_config():
        logger.warning("فشل التحقق من الإعدادات. يرجى التأكد من تكوين ملف .env بشكل صحيح.")
        return None, None, None
    
    try:
        # ----- تهيئة Vertex AI ----- 
        logger.info(f"جاري تهيئة Vertex AI باستخدام المشروع: {PROJECT_ID}")
        init_vertex(PROJECT_ID, REGION, KEY_PATH)
        
        # ----- نشر نموذج Gemini من Model Garden ----- 
        logger.info("جاري نشر نموذج Gemini...")
        endpoint = deploy_model("gemini-2.5-flash", IMAGE_URI)
        
        # ----- تهيئة أنظمة الذاكرة ----- 
        logger.info(f"جاري تهيئة الذاكرة العاملة باستخدام: {REDIS_HOST}")
        working_mem = init_working_memory(REDIS_HOST)
        
        logger.info("جاري تهيئة الذاكرة طويلة المدى...")
        long_mem = init_long_term_memory()
        
        logger.info("تم تهيئة جميع الخدمات بنجاح!")
        return endpoint, working_mem, long_mem
    except Exception as e:
        logger.error(f"حدث خطأ أثناء التهيئة: {str(e)}")
        return None, None, None

# تهيئة الخدمات
endpoint, working_mem, long_mem = initialize_services()

# ----- دوال التحليل ----- 
def deep_analysis(text):
    return call_gemini(endpoint, f"تحليل فلسفي: {text}")

def logical_analysis(text):
    return call_gemini(endpoint, f"تحليل منطقي: {text}")

# ----- تنفيذ التحليلات المتوازية ----- 
def run_parallel(jobs):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(job) for job in jobs]
        return [f.result() for f in futures]

# ----- التدفق الرئيسي ----- 
def main(user_input, chat_history):
    # استرجاع السياق والتذكير
    reminder = context_reminder(user_input, chat_history, long_mem, working_mem)
    
    # تنفيذ التحليلات بشكل متوازي
    analyses = run_parallel([
        lambda: deep_analysis(reminder + user_input),
        lambda: logical_analysis(reminder + user_input),
    ])
    
    # دمج النتائج
    final = call_gemini(endpoint, f"دمج النتائج: {analyses}")
    
    # تخزين المدخلات في الذاكرة طويلة المدى
    long_mem.add(documents=[user_input], metadatas=[{"time": datetime.now().isoformat()}])
    
    return final

# ----- نقطة البداية ----- 
if __name__ == "__main__":
    if None in (endpoint, working_mem, long_mem):
        logger.error("لم يتم تهيئة الخدمات بشكل صحيح. يرجى التحقق من الإعدادات وإعادة المحاولة.")
    else:
        try:
            user_input = input("أدخل النص للتحليل: ")
            chat_history = []
            logger.info("جاري تحليل النص...")
            result = main(user_input, chat_history)
            print("\n=== نتيجة التحليل ===")
            print(result)
            logger.info("تم إكمال التحليل بنجاح!")
        except Exception as e:
            logger.error(f"حدث خطأ أثناء التنفيذ: {str(e)}")
            print("حدث خطأ أثناء تنفيذ التحليل. يرجى التحقق من سجل الأخطاء للمزيد من المعلومات.")