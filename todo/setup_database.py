#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
إعداد قاعدة البيانات لوكيل قائمة المهام
"""

import mysql.connector
import sys
import logging
from config import DB_CONFIG

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) # Ensure output goes to stdout
    ]
)
logger = logging.getLogger("setup_database")

def setup_database():
    """
    إنشاء قاعدة البيانات والجداول اللازمة
    """
    conn = None
    cursor = None
    try:
        logger.info(f"محاولة الاتصال بخادم MySQL على {DB_CONFIG['host']}:{DB_CONFIG['port']} كمستخدم {DB_CONFIG['user']}")
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            charset='utf8mb4' # Specify charset for connection
        )
        cursor = conn.cursor()
        
        logger.info(f"إنشاء قاعدة البيانات {DB_CONFIG['database']} إذا لم تكن موجودة")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        cursor.execute(f"USE {DB_CONFIG['database']}")
        logger.info(f"تم تحديد قاعدة البيانات {DB_CONFIG['database']}.")
        
        logger.info("إنشاء جدول sessions")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP NULL DEFAULT NULL,
            session_summary VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL
        )
        """)
        
        logger.info("إنشاء جدول messages")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            sender VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) 
                REFERENCES sessions(session_id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)
        
        logger.info("إنشاء جدول tasks")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            task_text VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            section VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
            status ENUM('pending', 'completed') NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL DEFAULT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        
        logger.info("إنشاء الفهارس")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sender ON messages(sender)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_start_time ON sessions(start_time)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_task_section ON tasks(section)")
        
        conn.commit()
        logger.info("تم إعداد قاعدة البيانات والجداول بنجاح!")
        
        logger.info("إنشاء جلسة أولية")
        cursor.execute(
            "INSERT INTO sessions (session_summary) VALUES (%s)",
            ("جلسة إعداد قائمة المهام",)
        )
        session_id = cursor.lastrowid
        
        cursor.execute(
            "INSERT INTO messages (session_id, sender, content) VALUES (%s, %s, %s)",
            (session_id, "system", "تم إنشاء وكيل قائمة المهام وربطه بقاعدة البيانات")
        )
        
        conn.commit()
        return True
    
    except mysql.connector.Error as err:
        logger.error(f"خطأ في إعداد قاعدة البيانات: {err}")
        if conn and conn.is_connected():
            try:
                conn.rollback()
                logger.info("تم التراجع عن التغييرات بسبب الخطأ.")
            except Exception as e_rollback:
                logger.error(f"خطأ أثناء التراجع: {e_rollback}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("تم إغلاق الاتصال بقاعدة البيانات.")

def test_connection():
    """
    اختبار الاتصال بقاعدة البيانات
    """
    conn = None
    cursor = None
    try:
        logger.info(f"محاولة اختبار الاتصال بـ {DB_CONFIG['database']} على {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        conn = mysql.connector.connect(**DB_CONFIG, charset='utf8mb4')
        if conn.is_connected():
            logger.info("تم الاتصال بقاعدة البيانات بنجاح!")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessions")
            session_count = cursor.fetchone()[0]
            logger.info(f"عدد الجلسات الحالية: {session_count}")
            cursor.execute("SELECT COUNT(*) FROM messages")
            message_count = cursor.fetchone()[0]
            logger.info(f"عدد الرسائل الحالية: {message_count}")
            return True
    except mysql.connector.Error as err:
        logger.error(f"خطأ في الاتصال بقاعدة البيانات: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    print("=== إعداد قاعدة بيانات وكيل قائمة المهام ===")
    
    print(f"الخادم: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"قاعدة البيانات: {DB_CONFIG['database']}")
    print(f"المستخدم: {DB_CONFIG['user']}")
    
    logger.info("البدء في إعداد قاعدة البيانات بدون تأكيد مسبق.")
    
    if setup_database():
        print("\nتم إعداد قاعدة البيانات بنجاح!")
        print("\nجارٍ اختبار الاتصال...")
        if test_connection():
            print("تم اختبار الاتصال بنجاح.")
        else:
            print("فشل اختبار الاتصال.")
            sys.exit(1)
    else:
        print("\nفشل إعداد قاعدة البيانات. راجع السجلات لمزيد من المعلومات.")
        sys.exit(1)
