# config.py
"""
ملف الإعدادات لمشروع Horus AI Pipeline
يقوم بتحميل متغيرات البيئة من ملف .env والتحقق من صحتها
"""

import os
import logging
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# استخراج متغيرات البيئة مع توفير قيم افتراضية
PROJECT_ID = os.getenv('PROJECT_ID', 'horus-ai-pipeline')
REGION = os.getenv('REGION', 'us-central1')
KEY_PATH = os.getenv('KEY_PATH', '')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

# إعدادات النماذج
MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-flash')
IMAGE_URI = os.getenv(
    'IMAGE_URI',
    'us-docker.pkg.dev/vertex-ai/prediction/gemini-1.5-flash:latest'
)

# إعدادات النماذج المتعددة للجزء الثاني
MODELS = {
    "fast": os.getenv("FAST_MODEL", "gemini-1.5-flash"),
    "analysis": os.getenv("ANALYSIS_MODEL", "gemini-1.5-pro"),
    "deep_thinking": os.getenv("DEEP_MODEL", "gemini-1.5-pro"),
    "summary": os.getenv("SUMMARY_MODEL", "gemini-1.5-flash")
}


def validate_config(check_key_path=True):
    """
    التحقق من صحة الإعدادات

    Args:
        check_key_path (bool): ما إذا كان يجب التحقق من وجود ملف مفتاح الخدمة
            (يمكن تعيينه على False عند التشغيل في Google Cloud)

    Returns:
        bool: True إذا كانت الإعدادات صحيحة، False خلاف ذلك
    """
    missing_vars = []
    warnings = []

    # التحقق من المتغيرات الأساسية
    if not PROJECT_ID:
        missing_vars.append('PROJECT_ID')

    # التحقق من ملف المفتاح
    if check_key_path and KEY_PATH and not os.path.exists(KEY_PATH):
        warnings.append(f"ملف المفتاح غير موجود: {KEY_PATH}")

    # عرض التحذيرات والأخطاء
    if warnings:
        for warning in warnings:
            logger.warning(f"⚠️ تحذير: {warning}")

    if missing_vars:
        logger.error(
            f"❌ خطأ: المتغيرات التالية مفقودة: {', '.join(missing_vars)}"
        )
        logger.error("يرجى تعديل ملف .env بالقيم الصحيحة.")
        return False

    # تسجيل معلومات الإعدادات
    logger.info(
        f"✅ تم التحقق من الإعدادات بنجاح. "
        f"المشروع: {PROJECT_ID}, المنطقة: {REGION}"
    )
    logger.info(f"النموذج الافتراضي: {MODEL_NAME}")

    return True


def get_config_dict():
    """
    الحصول على الإعدادات كقاموس

    Returns:
        dict: قاموس يحتوي على جميع الإعدادات
    """
    return {
        "PROJECT_ID": PROJECT_ID,
        "REGION": REGION,
        "KEY_PATH": KEY_PATH,
        "REDIS_HOST": REDIS_HOST,
        "REDIS_PORT": REDIS_PORT,
        "MODEL_NAME": MODEL_NAME,
        "IMAGE_URI": IMAGE_URI,
        "MODELS": MODELS
    }