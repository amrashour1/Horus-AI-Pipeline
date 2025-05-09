#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
u0633u0643u0631u064au0628u062a u0625u0639u062fu0627u062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0644u0645u0634u0631u0648u0639 Horus AI Pipeline

u064au0642u0648u0645 u0647u0630u0627 u0627u0644u0633u0643u0631u064au0628u062a u0628u0625u0646u0634u0627u0621 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0648u0627u0644u062cu062fu0627u0648u0644 u0627u0644u0644u0627u0632u0645u0629 u0644u0644u0645u0634u0631u0648u0639.
"""

import mysql.connector
import logging
import os
from db_config import DB_CONFIG

# u0625u0639u062fu0627u062f u0627u0644u062au0633u062cu064au0644
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database_setup.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("setup_database")

def read_sql_file(file_path):
    """u0642u0631u0627u0621u0629 u0645u0644u0641 SQL u0648u0627u0633u062au062eu0631u0627u062c u0627u0644u0627u0633u062au0639u0644u0627u0645u0627u062a"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # u062au0642u0633u064au0645 u0627u0644u0645u0644u0641 u0625u0644u0649 u0627u0633u062au0639u0644u0627u0645u0627u062a u0645u0646u0641u0635u0644u0629
        # u0646u0641u062au0631u0636 u0623u0646 u0627u0644u0627u0633u062au0639u0644u0627u0645u0627u062a u0645u0641u0635u0648u0644u0629 u0628u0648u0627u0633u0637u0629 ';'
        queries = [q.strip() for q in sql_content.split(';') if q.strip()]
        return queries
    except Exception as e:
        logger.error(f"u062eu0637u0623 u0641u064a u0642u0631u0627u0621u0629 u0645u0644u0641 SQL: {e}")
        return []

def setup_database():
    """u0625u0639u062fu0627u062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0648u0627u0644u062cu062fu0627u0648u0644"""
    # u0627u0644u062du0635u0648u0644 u0639u0644u0649 u0645u0633u0627u0631 u0645u0644u0641 SQL
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(current_dir, 'database_setup.sql')
    
    # u0642u0631u0627u0621u0629 u0627u0633u062au0639u0644u0627u0645u0627u062a SQL
    queries = read_sql_file(sql_file_path)
    if not queries:
        logger.error("u0644u0645 u064au062au0645 u0627u0644u0639u062bu0648u0631 u0639u0644u0649 u0627u0633u062au0639u0644u0627u0645u0627u062a SQL u0641u064a u0627u0644u0645u0644u0641")
        return False
    
    # u0625u0646u0634u0627u0621 u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
    try:
        # u0627u0644u0627u062au0635u0627u0644 u0628u062fu0648u0646 u062au062du062fu064au062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
        db_config = DB_CONFIG.copy()
        if 'database' in db_config:
            del db_config['database']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # u062au0646u0641u064au0630 u0627u0644u0627u0633u062au0639u0644u0627u0645 u0627u0644u0623u0648u0644 (u0625u0646u0634u0627u0621 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a)
        logger.info("u062cu0627u0631u064d u0625u0646u0634u0627u0621 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a...")
        cursor.execute(queries[0])
        
        # u0627u0633u062au062eu062fu0627u0645 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0627u0644u062au064a u062au0645 u0625u0646u0634u0627u0624u0647u0627
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # u062au0646u0641u064au0630 u0628u0642u064au0629 u0627u0644u0627u0633u062au0639u0644u0627u0645u0627u062a (u0625u0646u0634u0627u0621 u0627u0644u062cu062fu0627u0648u0644)
        for i, query in enumerate(queries[1:], 1):
            if query.strip():
                logger.info(f"u062cu0627u0631u064d u062au0646u0641u064au0630 u0627u0644u0627u0633u062au0639u0644u0627u0645 {i}: {query[:50]}...")
                cursor.execute(query)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("u062au0645 u0625u0639u062fu0627u062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0628u0646u062cu0627u062d!")
        return True
    
    except mysql.connector.Error as err:
        logger.error(f"u062eu0637u0623 u0641u064a u0625u0639u062fu0627u062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a: {err}")
        return False

def verify_database_setup():
    """u0627u0644u062au062du0642u0642 u0645u0646 u0625u0639u062fu0627u062f u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a"""
    try:
        # u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # u0627u0644u062au062du0642u0642 u0645u0646 u0648u062cu0648u062f u0627u0644u062cu062fu0627u0648u0644
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        expected_tables = ['sessions', 'messages']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            logger.warning(f"u0627u0644u062cu062fu0627u0648u0644 u0627u0644u0645u0641u0642u0648u062fu0629: {', '.join(missing_tables)}")
            return False
        
        # u0627u0644u062au062du0642u0642 u0645u0646 u0647u064au0643u0644 u0627u0644u062cu062fu0648u0644
        for table in expected_tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            logger.info(f"جدول {table} يحتوي على {len(columns)} عمود")
        
        cursor.close()
        conn.close()
        
        logger.info("تم التحقق من إعداد قاعدة البيانات بنجاح!")
        return True
    
    except mysql.connector.Error as err:
        logger.error(f"خطأ في التحقق من إعداد قاعدة البيانات: {err}")
        return False

def test_connection():
    """اختبار الاتصال بقاعدة البيانات قبل إعداد الجداول"""
    try:
        # الاتصال بدون تحديد قاعدة البيانات
        db_config = DB_CONFIG.copy()
        if 'database' in db_config:
            del db_config['database']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result and result[0] == 1:
            logger.info("تم الاتصال بخادم MySQL بنجاح")
            return True
        else:
            logger.warning("فشل الاتصال بخادم MySQL")
            return False
    except mysql.connector.Error as err:
        logger.error(f"خطأ في الاتصال بخادم MySQL: {err}")
        return False

if __name__ == "__main__":
    print("جارٍ إعداد قاعدة البيانات لمشروع Horus AI Pipeline...")
    
    # اختبار الاتصال أولاً
    if test_connection():
        print("تم الاتصال بخادم MySQL بنجاح!")
        
        # إعداد قاعدة البيانات
        if setup_database():
            print("تم إعداد قاعدة البيانات بنجاح!")
            
            # التحقق من الإعداد
            if verify_database_setup():
                print("تم التحقق من إعداد قاعدة البيانات بنجاح!")
            else:
                print("حدث خطأ في التحقق من إعداد قاعدة البيانات.")
        else:
            print("حدث خطأ في إعداد قاعدة البيانات.")
    else:
        print("فشل الاتصال بخادم MySQL. تأكد من تشغيل خادم MySQL وصحة بيانات الاتصال.")
        print("راجع ملف db_config.py للتأكد من صحة إعدادات الاتصال.")
