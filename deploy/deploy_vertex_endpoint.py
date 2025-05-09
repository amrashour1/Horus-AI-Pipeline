"""
سكريبت لنشر نقطة نهاية Vertex AI
"""

import os
import logging
from dotenv import load_dotenv
from google.cloud import aiplatform

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
IMAGE_URI = os.getenv("IMAGE_URI")

def deploy_gemini_endpoint(model_name="gemini-1.5-flash", machine_type="n1-standard-4"):
    """
    نشر نموذج Gemini كنقطة نهاية Vertex AI
    """
    # تهيئة Vertex AI
    if KEY_PATH and os.path.exists(KEY_PATH):
        aiplatform.init(
            project=PROJECT_ID,
            location=REGION,
            credentials=KEY_PATH,
        )
    else:
        aiplatform.init(
            project=PROJECT_ID,
            location=REGION,
        )
    
    logger.info(f"جاري نشر نموذج {model_name} كنقطة نهاية Vertex AI...")
    
    # تحديد URI الصورة بناءً على اسم النموذج
    if "gemini-1.5-flash" in model_name:
        container_uri = "us-docker.pkg.dev/vertex-ai/prediction/gemini-1.5-flash:latest"
    elif "gemini-1.5-pro" in model_name:
        container_uri = "us-docker.pkg.dev/vertex-ai/prediction/gemini-1.5-pro:latest"
    else:
        container_uri = IMAGE_URI
    
    # تحميل النموذج
    model = aiplatform.Model.upload(
        display_name=f"horus-{model_name}",
        serving_container_image_uri=container_uri,
    )
    
    # نشر النموذج كنقطة نهاية
    endpoint = model.deploy(
        machine_type=machine_type,
        min_replica_count=1,
        max_replica_count=2,
        traffic_split={"0": 100},
    )
    
    logger.info(f"تم نشر النموذج بنجاح! معرف نقطة النهاية: {endpoint.name}")
    logger.info(f"URI نقطة النهاية: {endpoint.resource_name}")
    
    return endpoint

def main():
    """الدالة الرئيسية"""
    print("=== نشر نقطة نهاية Vertex AI لنموذج Gemini ===")
    
    # التحقق من المتغيرات المطلوبة
    if not PROJECT_ID or not REGION:
        print("خطأ: يجب تعيين PROJECT_ID و REGION في ملف .env")
        return
    
    # طلب معلومات النشر من المستخدم
    print("\nالنماذج المتاحة:")
    print("1. gemini-1.5-flash (سريع، خفيف)")
    print("2. gemini-1.5-pro (متقدم، أكثر قدرة)")
    
    choice = input("\nاختر النموذج (1 أو 2): ")
    model_name = "gemini-1.5-flash" if choice == "1" else "gemini-1.5-pro"
    
    print("\nأنواع الآلات المتاحة:")
    print("1. n1-standard-2 (2 vCPU, 7.5 GB)")
    print("2. n1-standard-4 (4 vCPU, 15 GB)")
    print("3. n1-standard-8 (8 vCPU, 30 GB)")
    
    machine_choice = input("\nاختر نوع الآلة (1-3): ")
    if machine_choice == "1":
        machine_type = "n1-standard-2"
    elif machine_choice == "3":
        machine_type = "n1-standard-8"
    else:
        machine_type = "n1-standard-4"
    
    # تأكيد النشر
    print(f"\nسيتم نشر النموذج {model_name} على آلة من نوع {machine_type}")
    confirm = input("هل تريد المتابعة؟ (y/n): ")
    
    if confirm.lower() != "y":
        print("تم إلغاء النشر.")
        return
    
    # نشر النموذج
    try:
        endpoint = deploy_gemini_endpoint(model_name, machine_type)
        print("\nتم نشر النموذج بنجاح!")
        print(f"معرف نقطة النهاية: {endpoint.name}")
        print(f"URI نقطة النهاية: {endpoint.resource_name}")
        
        # حفظ معلومات نقطة النهاية في ملف
        with open("endpoint_info.txt", "w") as f:
            f.write(f"MODEL_NAME={model_name}\n")
            f.write(f"ENDPOINT_ID={endpoint.name}\n")
            f.write(f"ENDPOINT_URI={endpoint.resource_name}\n")
        
        print("\nتم حفظ معلومات نقطة النهاية في ملف endpoint_info.txt")
    except Exception as e:
        print(f"خطأ في نشر النموذج: {str(e)}")

if __name__ == "__main__":
    main()
