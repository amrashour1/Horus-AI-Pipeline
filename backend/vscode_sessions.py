#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لتسجيل جلسات VS Code الحالية
"""

import os
import json
import sqlite3
from datetime import datetime
from db_manager import DatabaseManager
import logging

# تكوين التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_vscode_sessions():
    try:
        # مسار ملف جلسات VS Code (يختلف حسب نظام التشغيل)
        session_path = os.path.expanduser('~\\AppData\\Roaming\\Code\\User\\workspaceStorage')
        
        if not os.path.exists(session_path):
            logger.error("لم يتم العثور على مجلد جلسات VS Code")
            return []

        sessions = []
        for dir_name in os.listdir(session_path):
            workspace_file = os.path.join(session_path, dir_name, 'workspace.json')
            if os.path.exists(workspace_file):
                try:
                    with open(workspace_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        folder = data.get('folder', '')
                        if folder.startswith('file:///'):
                            folder = folder[8:]  # إزالة البادئة file://
                        sessions.append({
                            'folder': folder,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف الجلسة: {e}")
        
        return sessions

    except Exception as e:
        logger.error(f"حدث خطأ أثناء جلب الجلسات: {e}")
        return []

def save_sessions_to_db(sessions):
    try:
        db = DatabaseManager()
        
        for session in sessions:
            # إضافة الجلسة إلى قاعدة البيانات
            session_id = db.add_session(
                start_time=session['timestamp'],
                session_summary=f"جلسة VS Code: {session['folder']}"
            )
            
            # إضافة رسالة افتراضية للجلسة
            db.add_message(
                session_id=session_id,
                sender="system",
                content=f"بدأت جلسة جديدة في المجلد: {session['folder']}"
            )
            
            logger.info(f"تم حفظ جلسة: {session['folder']}")
            
        logger.info("تم حفظ جميع الجلسات بنجاح")
        return True
        
    except Exception as e:
        logger.error(f"حدث خطأ أثناء حفظ الجلسات: {e}")
        return False

def main():
    logger.info("جاري البحث عن جلسات VS Code...")
    sessions = get_vscode_sessions()
    
    if not sessions:
        logger.warning("لم يتم العثور على أي جلسات VS Code نشطة")
        return
    
    logger.info(f"تم العثور على {len(sessions)} جلسة")
    save_sessions_to_db(sessions)

if __name__ == "__main__":
    main()