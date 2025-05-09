"""
اختبار للتحقق من تثبيت المكتبات المطلوبة
"""

import sys
import importlib.util

def test_module_installed(module_name):
    """التحقق من تثبيت وحدة معينة"""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ وحدة {module_name} غير مثبتة")
        return False
    else:
        print(f"✅ وحدة {module_name} مثبتة")
        return True

def main():
    """الدالة الرئيسية"""
    print("=== التحقق من تثبيت المكتبات المطلوبة ===\n")
    
    # قائمة المكتبات المطلوبة
    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "google-generativeai",
        "google-cloud-aiplatform",
        "google-auth",
        "redis"
    ]
    
    # التحقق من تثبيت كل مكتبة
    all_installed = True
    for module in required_modules:
        if not test_module_installed(module):
            all_installed = False
    
    # طباعة النتيجة النهائية
    print("\n=== النتيجة النهائية ===")
    if all_installed:
        print("✅ جميع المكتبات المطلوبة مثبتة")
    else:
        print("❌ بعض المكتبات المطلوبة غير مثبتة")
        print("قم بتثبيت المكتبات المطلوبة باستخدام:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
