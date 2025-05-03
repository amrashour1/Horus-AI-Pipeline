# config.py

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# استخراج متغيرات البيئة مع توفير قيم افتراضية
PROJECT_ID = os.getenv('PROJECT_ID', 'your-project-id')
REGION = os.getenv('REGION', 'us-central1')
KEY_PATH = os.getenv('KEY_PATH', 'path/to/your-key.json')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
IMAGE_URI = os.getenv('IMAGE_URI', 'us-docker.pkg.dev/vertex-ai/prediction/gemini-2.5-flash:latest')

# التحقق من وجود المتغيرات الضرورية
def validate_config():
    missing_vars = []
    if PROJECT_ID == 'your-project-id':
        missing_vars.append('PROJECT_ID')
    if KEY_PATH == 'path/to/your-key.json' or not os.path.exists(KEY_PATH):
        missing_vars.append('KEY_PATH')
    
    if missing_vars:
        print(f"⚠️ تحذير: المتغيرات التالية غير معرفة أو غير صحيحة: {', '.join(missing_vars)}")
        print("يرجى تعديل ملف .env بالقيم الصحيحة.")
        return False
    return True