#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
مدير الجلسات لمشروع Horus AI Pipeline

يوفر هذا الملف وظائف لإدارة الجلسات وحفظها في قاعدة البيانات.
"""

from datetime import datetime
from db_manager import DatabaseManager
import logging

# إعداد التسجيل
logger = logging.getLogger("session_manager")

class SessionManager:
    """
    مدير الجلسات للتعامل مع عمليات حفظ واسترجاع الجلسات من قاعدة البيانات
    """
    
    def __init__(self):
        """تهيئة مدير الجلسات"""
        self.db = DatabaseManager()
    
    def create_session(self):
        """
        إنشاء جلسة جديدة في قاعدة البيانات
        
        العائد:
            int: معرف الجلسة الجديدة أو None في حالة الفشل
        """
        try:
            start_time = datetime.now()
            query = """
            INSERT INTO sessions (start_time)
            VALUES (%s)
            """
            session_id = self.db.execute_query(query, (start_time,), fetch_lastrowid=True)
            logger.info(f"تم إنشاء جلسة جديدة برقم: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"خطأ في إنشاء جلسة جديدة: {str(e)}")
            return None
    
    def end_session(self, session_id):
        """
        إنهاء جلسة موجودة
        
        المعلمات:
            session_id (int): معرف الجلسة
            
        العائد:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        try:
            end_time = datetime.now()
            query = """
            UPDATE sessions 
            SET end_time = %s
            WHERE session_id = %s
            """
            self.db.execute_query(query, (end_time, session_id))
            logger.info(f"تم إنهاء الجلسة رقم: {session_id}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إنهاء الجلسة {session_id}: {str(e)}")
            return False
    
    def add_message(self, session_id, sender, content):
        """
        إضافة رسالة إلى الجلسة
        
        المعلمات:
            session_id (int): معرف الجلسة
            sender (str): مرسل الرسالة (مستخدم أو نظام)
            content (str): محتوى الرسالة
            
        العائد:
            int: معرف الرسالة الجديدة أو None في حالة الفشل
        """
        try:
            timestamp = datetime.now()
            query = """
            INSERT INTO messages (session_id, sender, content, timestamp)
            VALUES (%s, %s, %s, %s)
            """
            message_id = self.db.execute_query(
                query, 
                (session_id, sender, content, timestamp),
                fetch_lastrowid=True
            )
            logger.debug(f"تمت إضافة رسالة للجلسة {session_id}")
            return message_id
        except Exception as e:
            logger.error(f"خطأ في إضافة رسالة للجلسة {session_id}: {str(e)}")
            return None
    
    def get_session_messages(self, session_id):
        """
        استرجاع جميع رسائل جلسة محددة
        
        المعلمات:
            session_id (int): معرف الجلسة
            
        العائد:
            list: قائمة بالرسائل أو قائمة فارغة في حالة عدم وجود رسائل
        """
        try:
            query = """
            SELECT message_id, sender, content, timestamp
            FROM messages
            WHERE session_id = %s
            ORDER BY timestamp ASC
            """
            messages = self.db.execute_query(query, (session_id,), fetch=True)
            return messages or []
        except Exception as e:
            logger.error(f"خطأ في استرجاع رسائل الجلسة {session_id}: {str(e)}")
            return []
    
    def get_all_sessions(self):
        """
        استرجاع جميع الجلسات المحفوظة
        
        العائد:
            list: قائمة بالجلسات أو قائمة فارغة في حالة عدم وجود جلسات
        """
        try:
            query = """
            SELECT s.session_id, s.start_time, s.end_time, s.session_summary,
                   COUNT(m.message_id) as message_count
            FROM sessions s
            LEFT JOIN messages m ON s.session_id = m.session_id
            GROUP BY s.session_id
            ORDER BY s.start_time DESC
            """
            sessions = self.db.execute_query(query, fetch=True)
            return sessions or []
        except Exception as e:
            logger.error(f"خطأ في استرجاع الجلسات: {str(e)}")
            return []


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء مدير الجلسات
    session_mgr = SessionManager()
    
    # إنشاء جلسة جديدة
    session_id = session_mgr.create_session()
    print(f"تم إنشاء جلسة جديدة برقم: {session_id}")
    
    if session_id:
        # إضافة رسائل للجلسة
        session_mgr.add_message(session_id, "نظام", "مرحباً بك في نظام Horus AI")
        session_mgr.add_message(session_id, "مستخدم", "شكراً، أريد مساعدة في مشروعي")
        
        # استعراض رسائل الجلسة
        print("\nرسائل الجلسة:")
        messages = session_mgr.get_session_messages(session_id)
        for msg in messages:
            print(f"{msg['timestamp']} - {msg['sender']}: {msg['content']}")
        
        # إنهاء الجلسة
        session_mgr.end_session(session_id)
        print("\nتم إنهاء الجلسة بنجاح")


def create_session(session_summary):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (session_summary) VALUES (%s)",
            (session_summary,)
        )
        session_id = cursor.lastrowid
        conn.commit()
        return session_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_message(session_id, sender, content):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, sender, content) VALUES (%s, %s, %s)",
            (session_id, sender, content)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
