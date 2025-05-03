# my_mcp_server.py
"""
خادم MCP (Master Control Program) محسّن مع ميزات إضافية.
يوفر واجهة API لتنفيذ أدوات مختلفة وتتبع تاريخ الطلبات.
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, HTTPException, Depends, Header
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

app = FastAPI(title="Augmented MCP Server",
              description="An enhanced MCP (Master Control Program) server with additional features",
              version="1.0.0")

# Define request models

class ToolRequest(BaseModel):
    """طلب تنفيذ أداة.

    Attributes:
        tool_name: اسم الأداة المطلوب تنفيذها
        parameters: معلمات الأداة
        request_id: معرف الطلب (اختياري)
    """
    tool_name: str
    parameters: Dict[str, Any]
    request_id: Optional[str] = None


class ToolResponse(BaseModel):
    """استجابة لطلب تنفيذ أداة.

    Attributes:
        response: رسالة الاستجابة
        request_id: معرف الطلب
        status: حالة التنفيذ (نجاح أو خطأ)
        execution_time: وقت التنفيذ بالثواني
        data: بيانات النتيجة
    """
    response: str
    request_id: str
    status: str
    execution_time: float
    data: Dict[str, Any]

# In-memory storage for requests
request_history = []

# Middleware to log requests


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """وسيط لتسجيل الطلبات الواردة ووقت معالجتها.

    Args:
        request: كائن الطلب
        call_next: الدالة التالية في سلسلة المعالجة

    Returns:
        استجابة HTTP
    """
    request_id = str(uuid.uuid4())
    logger.info("Request %s started: %s %s", request_id, request.method, request.url)
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        "Request %s completed in %.4fs with status %d",
        request_id,
        process_time,
        response.status_code
    )

    return response

# Authentication dependency (simple API key check)


async def verify_api_key(x_api_key: str = Header(None)):
    """التحقق من صحة مفتاح API.

    Args:
        x_api_key: مفتاح API المقدم في رأس الطلب

    Returns:
        مفتاح API إذا كان صالحًا

    Raises:
        HTTPException: إذا كان مفتاح API غير صالح
    """
    if x_api_key != "your-secret-api-key":  # في الإنتاج، استخدم نهجًا أكثر أمانًا
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


@app.get("/")
async def root():
    """نقطة النهاية الجذرية التي تعرض حالة الخادم.

    Returns:
        معلومات حالة الخادم
    """
    return {"status": "MCP server is running", "version": "1.0.0"}


@app.post("/run-tool", response_model=ToolResponse)
async def run_tool(request: ToolRequest, api_key: str = Depends(verify_api_key)):
    """تنفيذ أداة محددة.

    Args:
        request: طلب تنفيذ الأداة
        api_key: مفتاح API (يتم التحقق منه تلقائيًا)

    Returns:
        نتيجة تنفيذ الأداة
    """
    start_time = time.time()
    logger.info("Processing tool request: %s", request.tool_name)

    # توليد معرف الطلب إذا لم يتم توفيره
    request_id = request.request_id or str(uuid.uuid4())

    # منطق تنفيذ الأداة بناءً على اسم الأداة
    result = {}
    try:
        # أداة الصدى
        if request.tool_name == "echo":
            result = {"echo": request.parameters}

        # أداة الحساب
        elif request.tool_name == "calculate":
            result = handle_calculate_tool(request.parameters)

        # أداة غير معروفة
        else:
            logger.warning("Unknown tool requested: %s", request.tool_name)
            result = {"error": f"Tool '{request.tool_name}' not found"}

    except Exception as e:
        logger.error("Error processing tool %s: %s", request.tool_name, str(e))
        execution_time = time.time() - start_time
        return ToolResponse(
            response=f"Error: {str(e)}",
            request_id=request_id,
            status="error",
            execution_time=execution_time,
            data={"error_details": str(e)}
        )

    # حساب وقت التنفيذ
    execution_time = time.time() - start_time

    # تخزين الطلب في السجل
    store_request_in_history(request_id, request.tool_name,
                            request.parameters, result)

    return ToolResponse(
        response=f"Successfully executed {request.tool_name}",
        request_id=request_id,
        status="success",
        execution_time=execution_time,
        data=result
    )


def handle_calculate_tool(parameters):
    """معالجة أداة الحساب.

    Args:
        parameters: معلمات الأداة

    Returns:
        نتيجة العملية الحسابية

    Raises:
        ValueError: إذا كانت المعلمات غير صالحة أو العملية غير مدعومة
    """
    if "operation" not in parameters or "values" not in parameters:
        raise ValueError("Missing required parameters for calculate tool")

    operation = parameters["operation"]
    values = parameters["values"]

    if operation == "sum":
        return {"result": sum(values)}
    elif operation == "multiply":
        product = 1
        for val in values:
            product *= val
        return {"result": product}
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def store_request_in_history(request_id, tool_name, parameters, result):
    """تخزين الطلب في سجل التاريخ.

    Args:
        request_id: معرف الطلب
        tool_name: اسم الأداة
        parameters: معلمات الأداة
        result: نتيجة التنفيذ
    """
    request_history.append({
        "request_id": request_id,
        "tool_name": tool_name,
        "parameters": parameters,
        "result": result,
        "timestamp": time.time()
    })

    # تحديد حجم السجل
    if len(request_history) > 100:
        request_history.pop(0)

@app.get("/history")
async def get_history(limit: int = 10, api_key: str = Depends(verify_api_key)):
    return {"history": request_history[-limit:]}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
