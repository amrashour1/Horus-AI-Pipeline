"""
واجهة برمجة تطبيقات بسيطة للاختبار
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Horus API Test",
    description="واجهة برمجة تطبيقات بسيطة للاختبار",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "مرحبًا بك في واجهة برمجة تطبيقات Horus للاختبار"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting simple API server on port 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
