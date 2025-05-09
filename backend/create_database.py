#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت بسيط لإنشاء قاعدة البيانات والجداول
"""

import mysql.connector
import sys
from db_config import DB_CONFIG

def create_database():
    """إنشاء قاعدة البيانات والجداول الأساسية"""
    try:
        # الاتصال بدون تحديد قاعدة البيانات
        db_config = DB_CONFIG.copy()
        if 'database' in db_config:
            database_name = db_config['database']
            del db_config['database']
        else:
            print("خطأ: لم يتم تحديد اسم قاعدة البيانات في ملف التكوين")
            return False
        
        print("جارٍ الاتصال بخادم MySQL...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # إنشاء قاعدة البيانات
        print(f"جارٍ إنشاء قاعدة البيانات {database_name}...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # استخدام قاعدة البيانات
        print(f"جارٍ استخدام قاعدة البيانات {database_name}...")
        cursor.execute(f"USE {database_name}")
        
        # إنشاء جدول sessions
        print("جارٍ إنشاء جدول sessions...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP NULL DEFAULT NULL,
            session_summary VARCHAR(255) NULL
        )
        """)
        
        # إنشاء جدول messages
        print("جارٍ إنشاء جدول messages...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            sender VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) 
                REFERENCES sessions(session_id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)
        
        # إنشاء الفهارس
        print("جارٍ إنشاء الفهارس...")
        try:
            cursor.execute("CREATE INDEX idx_session_id ON messages(session_id)")
        except mysql.connector.Error as err:
            print(f"تجاوز إنشاء فهرس idx_session_id: {err}")
        
        try:
            cursor.execute("CREATE INDEX idx_sender ON messages(sender)")
        except mysql.connector.Error as err:
            print(f"تجاوز إنشاء فهرس idx_sender: {err}")
        
        try:
            cursor.execute("CREATE INDEX idx_session_start_time ON sessions(start_time)")
        except mysql.connector.Error as err:
            print(f"تجاوز إنشاء فهرس idx_session_start_time: {err}")
        
        # إغلاق الاتصال
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ تم إنشاء قاعدة البيانات والجداول بنجاح!")
        return True
    
    except mysql.connector.Error as err:
        print(f"\n❌ خطأ في إنشاء قاعدة البيانات: {err}")
        return False

if __name__ == "__main__":
    print("=== إنشاء قاعدة بيانات Horus AI Pipeline ===")
    success = create_database()
    sys.exit(0 if success else 1)
