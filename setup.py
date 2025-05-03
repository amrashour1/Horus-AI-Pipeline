# setup.py

import os
import argparse
from dotenv import load_dotenv

def setup_project():
    # تحميل متغيرات البيئة من ملف .env إذا كان موجودًا
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ تم تحميل متغيرات البيئة من ملف .env")
    else:
        print("⚠️ ملف .env غير موجود. يرجى إنشاء ملف .env بناءً على نموذج .env.example")
    
    # التحقق من وجود مفتاح الخدمة
    key_path = os.getenv('KEY_PATH')
    if key_path and os.path.exists(key_path):
        print(f"✅ تم العثور على مفتاح الخدمة في: {key_path}")
    else:
        print("⚠️ مفتاح الخدمة غير موجود. يرجى إنشاء حساب خدمة وتوليد مفتاح JSON")
    
    # التحقق من تثبيت المكتبات المطلوبة
    print("\n📋 للتأكد من تثبيت جميع المكتبات المطلوبة، قم بتنفيذ:")
    print("pip install -r requirements.txt")
    
    # عرض معلومات حول تفعيل Google Cloud APIs
    print("\n🔧 لتفعيل Google Cloud APIs، قم بتنفيذ:")
    print("gcloud services enable aiplatform.googleapis.com storage.googleapis.com iam.googleapis.com")
    
    print("\n🚀 لتشغيل المشروع، قم بتنفيذ:")
    print("python horus_ai_pipeline.py")

def deploy_to_cloud(deploy_type):
    if deploy_type == 'run':
        print("\n🚀 لنشر المشروع على Cloud Run، قم بتنفيذ:")
        print("1. gcloud builds submit --tag gcr.io/PROJECT_ID/horus-ai")
        print("2. gcloud run deploy horus-ai --image gcr.io/PROJECT_ID/horus-ai --platform managed")
    elif deploy_type == 'app':
        print("\n🚀 لنشر المشروع على App Engine، قم بتنفيذ:")
        print("gcloud app deploy")
    else:
        print("\n⚠️ نوع النشر غير صالح. الخيارات المتاحة: 'run' أو 'app'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="إعداد ونشر مشروع Horus AI Pipeline")
    parser.add_argument('--deploy', choices=['run', 'app'], help="نشر المشروع على Google Cloud (run: Cloud Run, app: App Engine)")
    
    args = parser.parse_args()
    
    setup_project()
    
    if args.deploy:
        deploy_to_cloud(args.deploy)