"""
نقطة الدخول الرئيسية لحزمة Horus AI Pipeline
"""

import os
import sys
import argparse

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(description="Horus AI Pipeline")
    parser.add_argument("--mode", choices=["vertex", "gemini", "api", "orchestrator"],
                      default="gemini", help="وضع التشغيل")
    args = parser.parse_args()

    if args.mode == "vertex":
        from src.core.app import main as app_main
        app_main()
    elif args.mode == "gemini":
        from src.core.app_gemini import main as gemini_main
        gemini_main()
    elif args.mode == "api":
        from src.api.api import app
        import uvicorn
        import os
        port = int(os.getenv("PORT", 8080))
        uvicorn.run(app, host="0.0.0.0", port=port)
    elif args.mode == "orchestrator":
        from src.core.orchestrator import main as orchestrator_main
        orchestrator_main()

if __name__ == "__main__":
    main()
