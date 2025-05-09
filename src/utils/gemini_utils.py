"""
مكتبة للتعامل مع Gemini API من Google AI Studio
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_gemini_api():
    """
    تهيئة Gemini API باستخدام مفتاح API من Google AI Studio
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("لم يتم العثور على مفتاح API لـ Gemini. تأكد من وجود GEMINI_API_KEY في ملف .env")
        return False
    
    try:
        genai.configure(api_key=api_key)
        logger.info("تم تهيئة Gemini API بنجاح")
        return True
    except Exception as e:
        logger.error(f"خطأ في تهيئة Gemini API: {str(e)}")
        return False

def get_gemini_model(model_name="gemini-1.5-flash"):
    """
    الحصول على نموذج Gemini
    """
    try:
        model = genai.GenerativeModel(model_name)
        logger.info(f"تم تحميل النموذج {model_name} بنجاح")
        return model
    except Exception as e:
        logger.error(f"خطأ في تحميل النموذج: {str(e)}")
        return None

def call_gemini_direct(model, prompt, temperature=0.7, max_output_tokens=1024):
    """
    استدعاء نموذج Gemini مباشرة
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            }
        )
        return response.text
    except Exception as e:
        logger.error(f"خطأ في استدعاء النموذج: {str(e)}")
        raise

def call_gemini_multimodal(model, text_prompt, image_data=None):
    """
    استدعاء نموذج Gemini مع دعم الصور
    """
    try:
        if image_data:
            response = model.generate_content([text_prompt, {"mime_type": "image/jpeg", "data": image_data}])
        else:
            response = model.generate_content(text_prompt)
        return response.text
    except Exception as e:
        logger.error(f"خطأ في استدعاء النموذج متعدد الوسائط: {str(e)}")
        raise
