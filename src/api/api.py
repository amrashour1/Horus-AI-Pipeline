"""
Horus AI Pipeline - واجهة برمجة التطبيقات (API)
للجزء الثاني من المشروع
"""

import os
import sys
import logging

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from dotenv import load_dotenv
    import uvicorn
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required packages using: pip install fastapi uvicorn python-dotenv pydantic")
    print("Or run the install-dependencies.bat script")
    sys.exit(1)

# إضافة مسار المشروع إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core import orchestrator

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Horus AI Pipeline API",
    description="واجهة برمجة التطبيقات لنظام Horus AI Pipeline متعدد النماذج",
    version="1.0.0",
    root_path="/"
)

# إضافة CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكن تعديلها للإنتاج لتكون أكثر تقييدًا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نماذج البيانات
class QueryRequest(BaseModel):
    query: str
    user_id: str = "anonymous"

class QueryResponse(BaseModel):
    response: str
    model_used: str = "multi-model"
    processing_time: float = 0.0

# تهيئة النظام عند بدء التشغيل
@app.on_event("startup")
async def startup_event():
    """تهيئة النظام عند بدء التشغيل"""
    logger.info("جاري تهيئة نظام Horus AI Pipeline...")
    if not orchestrator.initialize_system():
        logger.error("فشل في تهيئة النظام!")
    else:
        logger.info("تم تهيئة النظام بنجاح!")

# المسارات
@app.get("/")
async def root():
    """نقطة النهاية الرئيسية"""
    return {"message": "مرحبًا بك في واجهة برمجة تطبيقات Horus AI Pipeline"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """معالجة استعلام المستخدم"""
    try:
        import time
        start_time = time.time()

        # معالجة الاستعلام
        response = orchestrator.process_query(request.query)

        # حساب وقت المعالجة
        processing_time = time.time() - start_time

        return QueryResponse(
            response=response,
            model_used="multi-model",
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"خطأ في معالجة الاستعلام: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة الاستعلام: {str(e)}")

@app.get("/models")
async def get_models():
    """الحصول على قائمة النماذج المتاحة"""
    return {"models": orchestrator.MODELS}

@app.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {"status": "healthy"}

# تشغيل التطبيق
if __name__ == "__main__":
    # تحديد المنفذ من متغيرات البيئة أو استخدام 8080 كقيمة افتراضية
    port = int(os.getenv("PORT", 8080))

    # تشغيل خادم uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
