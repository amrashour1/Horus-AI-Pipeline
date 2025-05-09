#!/usr/bin/env python
"""
نقطة الدخول الرئيسية لمشروع Horus AI Pipeline
"""

import os
import sys
import argparse

# إضافة مسار المشروع إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
        try:
            from src.api.api import app
            import uvicorn
            import os
            port = int(os.getenv("PORT", 8080))
            print(f"Starting API server on port {port}...")
            uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        except ImportError as e:
            print(f"Error: {e}")
            print("Please install required packages using: pip install fastapi uvicorn python-dotenv pydantic")
            print("Or run the install-dependencies.bat script")
    elif args.mode == "orchestrator":
        from src.core.orchestrator import main as orchestrator_main
        orchestrator_main()

if __name__ == "__main__":
    main()
