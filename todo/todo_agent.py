#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
وكيل الذكاء الاصطناعي لإدارة قائمة المهام في مشروع Horus AI Pipeline

هذا الوكيل يقوم بتحديث قائمة المهام وربطها بقاعدة البيانات، مع القدرة على:
1. تحديث حالة المهام (مكتملة/غير مكتملة)
2. إضافة مهام جديدة
3. تتبع تقدم المشروع
4. حفظ المعلومات في قاعدة البيانات
"""

import os
import re
import sys
import json
import logging
import datetime
import mysql.connector
from pathlib import Path

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("todo_agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("todo_agent")

# تكوين قاعدة البيانات
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),  # يجب تعيين كلمة المرور الصحيحة
    "database": os.getenv("DB_NAME", "windsurf_pro_hours")
}

# مسار ملف قائمة المهام
TODO_FILE = Path(__file__).parent / "README.md"

# مسار ملف الذاكرة
MEMORY_FILE = Path(__file__).parent / "agent_memory.json"

class TodoAgent:
    """وكيل الذكاء الاصطناعي لإدارة قائمة المهام"""
    
    def __init__(self):
        """تهيئة الوكيل"""
        self.todo_content = ""
        self.working_memory = {}
        self.long_term_memory = self._load_memory()
        self.db_connection = None
        self._connect_to_db()
        self._load_todo_file()
        logger.info("تم تهيئة وكيل قائمة المهام بنجاح")
    
    def _connect_to_db(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.db_connection = mysql.connector.connect(**DB_CONFIG)
            logger.info("تم الاتصال بقاعدة البيانات بنجاح")
            return True
        except mysql.connector.Error as err:
            logger.error(f"فشل الاتصال بقاعدة البيانات: {err}")
            return False
    
    def _load_todo_file(self):
        """تحميل محتوى ملف قائمة المهام"""
        try:
            with open(TODO_FILE, "r", encoding="utf-8") as file:
                self.todo_content = file.read()
            logger.info("تم تحميل ملف قائمة المهام بنجاح")
            return True
        except Exception as e:
            logger.error(f"فشل تحميل ملف قائمة المهام: {e}")
            return False
    
    def _save_todo_file(self):
        """حفظ محتوى ملف قائمة المهام"""
        try:
            with open(TODO_FILE, "w", encoding="utf-8") as file:
                file.write(self.todo_content)
            logger.info("تم حفظ ملف قائمة المهام بنجاح")
            return True
        except Exception as e:
            logger.error(f"فشل حفظ ملف قائمة المهام: {e}")
            return False
    
    def _load_memory(self):
        """تحميل الذاكرة طويلة المدى"""
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"فشل تحميل ملف الذاكرة: {e}")
                return {}
        else:
            return {}
    
    def _save_memory(self):
        """حفظ الذاكرة طويلة المدى"""
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as file:
                json.dump(self.long_term_memory, file, ensure_ascii=False, indent=2)
            logger.info("تم حفظ الذاكرة بنجاح")
            return True
        except Exception as e:
            logger.error(f"فشل حفظ ملف الذاكرة: {e}")
            return False
    
    def update_task_status(self, task_text, completed=True):
        """تحديث حالة مهمة"""
        # نمط للبحث عن المهمة (مع أو بدون علامة الإكمال)
        pattern = re.compile(r'- \[([ xX])\] ' + re.escape(task_text))
        
        # علامة الإكمال الجديدة
        new_mark = "x" if completed else " "
        
        # البحث عن المهمة وتحديثها
        if pattern.search(self.todo_content):
            updated_content = pattern.sub(f'- [{new_mark}] {task_text}', self.todo_content)
            self.todo_content = updated_content
            self._save_todo_file()
            
            # تحديث الذاكرة
            self.working_memory["last_updated_task"] = task_text
            self.working_memory["last_action"] = "update_status"
            
            # حفظ في قاعدة البيانات
            self._log_action_to_db("update_task", {
                "task": task_text,
                "status": "completed" if completed else "pending"
            })
            
            logger.info(f"تم تحديث حالة المهمة: {task_text} -> {new_mark}")
            return True
        else:
            logger.warning(f"لم يتم العثور على المهمة: {task_text}")
            return False
    
    def add_task(self, task_text, section, completed=False):
        """إضافة مهمة جديدة"""
        # البحث عن القسم
        section_pattern = re.compile(f"### {re.escape(section)}\s*\n")
        section_match = section_pattern.search(self.todo_content)
        
        if section_match:
            # علامة الإكمال
            mark = "x" if completed else " "
            new_task_line = f"- [{mark}] {task_text}\n"
            
            # إيجاد موضع إدراج المهمة الجديدة (بعد آخر مهمة في القسم)
            section_start = section_match.end()
            next_section = re.search(r"\n### ", self.todo_content[section_start:])
            
            if next_section:
                insert_pos = section_start + next_section.start()
            else:
                insert_pos = len(self.todo_content)
            
            # إدراج المهمة الجديدة
            updated_content = self.todo_content[:insert_pos] + new_task_line + self.todo_content[insert_pos:]
            self.todo_content = updated_content
            self._save_todo_file()
            
            # تحديث الذاكرة
            self.working_memory["last_added_task"] = task_text
            self.working_memory["last_action"] = "add_task"
            
            # حفظ في قاعدة البيانات
            self._log_action_to_db("add_task", {
                "task": task_text,
                "section": section,
                "status": "completed" if completed else "pending"
            })
            
            logger.info(f"تمت إضافة مهمة جديدة: {task_text} في قسم {section}")
            return True
        else:
            logger.warning(f"لم يتم العثور على القسم: {section}")
            return False
    
    def add_section(self, section_name):
        """إضافة قسم جديد"""
        # التحقق من وجود القسم
        if f"### {section_name}" in self.todo_content:
            logger.warning(f"القسم موجود بالفعل: {section_name}")
            return False
        
        # إضافة القسم الجديد في نهاية الملف
        new_section = f"\n### {section_name}\n\n"
        self.todo_content += new_section
        self._save_todo_file()
        
        # تحديث الذاكرة
        self.working_memory["last_added_section"] = section_name
        self.working_memory["last_action"] = "add_section"
        
        # حفظ في قاعدة البيانات
        self._log_action_to_db("add_section", {"section": section_name})
        
        logger.info(f"تمت إضافة قسم جديد: {section_name}")
        return True
    
    def get_project_status(self):
        """الحصول على حالة المشروع الحالية"""
        # البحث عن جميع المهام
        task_pattern = re.compile(r'- \[([xX ])\] (.+)$', re.MULTILINE)
        tasks = task_pattern.findall(self.todo_content)
        
        # حساب الإحصائيات
        total_tasks = len(tasks)
        completed_tasks = sum(1 for status, _ in tasks if status.lower() == 'x')
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # تجميع المهام حسب الأقسام
        section_pattern = re.compile(r'### (.+)\s*\n([\s\S]*?)(?=\n### |$)')
        sections = section_pattern.findall(self.todo_content)
        
        section_stats = {}
        for section_name, section_content in sections:
            section_tasks = task_pattern.findall(section_content)
            section_total = len(section_tasks)
            section_completed = sum(1 for status, _ in section_tasks if status.lower() == 'x')
            section_percentage = (section_completed / section_total * 100) if section_total > 0 else 0
            
            section_stats[section_name] = {
                "total": section_total,
                "completed": section_completed,
                "percentage": section_percentage
            }
        
        # تحديث الذاكرة
        self.working_memory["last_status_check"] = datetime.datetime.now().isoformat()
        self.working_memory["project_completion"] = completion_percentage
        
        # حفظ في الذاكرة طويلة المدى
        self.long_term_memory["status_history"] = self.long_term_memory.get("status_history", [])
        self.long_term_memory["status_history"].append({
            "date": datetime.datetime.now().isoformat(),
            "completion": completion_percentage,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks
        })
        self._save_memory()
        
        # حفظ في قاعدة البيانات
        self._log_action_to_db("status_check", {
            "completion": completion_percentage,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks
        })
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_percentage": completion_percentage,
            "sections": section_stats
        }

    def search_task(self, search_text):
        """البحث عن مهمة معينة"""
        pattern = re.compile(r'- \[([xX ])\] (.+)')
        matches = pattern.findall(self.todo_content)
        found_tasks = [task for status, task in matches if search_text in task]
        
        if found_tasks:
            logger.info(f"تم العثور على المهام: {found_tasks}")
            return found_tasks
        else:
            logger.warning(f"لم يتم العثور على أي مهام تحتوي على: {search_text}")
            return []

    def delete_task(self, task_text):
        """حذف مهمة معينة"""
        pattern = re.compile(r'- \[([xX ])\] ' + re.escape(task_text) + r'\s*\n?')
        
        if pattern.search(self.todo_content):
            self.todo_content = pattern.sub('', self.todo_content)
            self._save_todo_file()
            
            # تحديث الذاكرة
            self.working_memory["last_deleted_task"] = task_text
            self.working_memory["last_action"] = "delete_task"
            
            # حفظ في قاعدة البيانات
            self._log_action_to_db("delete_task", {
                "task": task_text
            })
            
            logger.info(f"تم حذف المهمة: {task_text}")
            return True
        else:
            logger.warning(f"لم يتم العثور على المهمة: {task_text}")
            return False

    def export_tasks(self, export_file):
        """تصدير قائمة المهام إلى ملف نصي"""
        try:
            with open(export_file, "w", encoding="utf-8") as file:
                file.write(self.todo_content)
            
            # تحديث الذاكرة
            self.working_memory["last_export_file"] = export_file
            self.working_memory["last_action"] = "export_tasks"
            
            # حفظ في قاعدة البيانات
            self._log_action_to_db("export_tasks", {
                "file": export_file
            })
            
            logger.info(f"تم تصدير قائمة المهام إلى: {export_file}")
            return True
        except Exception as e:
            logger.error(f"فشل تصدير قائمة المهام: {e}")
            return False
    
    def _log_action_to_db(self, action_type, data):
        """تسجيل الإجراء في قاعدة البيانات"""
        if not self.db_connection or not self.db_connection.is_connected():
            if not self._connect_to_db():
                return False
        
        try:
            cursor = self.db_connection.cursor()
            
            # التحقق من وجود جلسة نشطة أو إنشاء واحدة جديدة
            cursor.execute(
                "SELECT session_id FROM sessions WHERE end_time IS NULL ORDER BY start_time DESC LIMIT 1"
            )
            session_result = cursor.fetchone()
            
            if session_result:
                session_id = session_result[0]
            else:
                # إنشاء جلسة جديدة
                cursor.execute(
                    "INSERT INTO sessions (session_summary) VALUES (%s)",
                    ("جلسة تحديث قائمة المهام",)
                )
                session_id = cursor.lastrowid
            
            # تسجيل الإجراء كرسالة
            message_content = json.dumps({
                "action": action_type,
                "data": data
            }, ensure_ascii=False)
            
            cursor.execute(
                "INSERT INTO messages (session_id, sender, content) VALUES (%s, %s, %s)",
                (session_id, "todo_agent", message_content)
            )
            
            self.db_connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            logger.error(f"خطأ في تسجيل الإجراء في قاعدة البيانات: {err}")
            return False
    
    def close(self):
        """إغلاق الوكيل وتنظيف الموارد"""
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            logger.info("تم إغلاق الاتصال بقاعدة البيانات")
        self._save_memory()
        logger.info("تم إغلاق وكيل قائمة المهام")


def main():
    """الدالة الرئيسية لتشغيل الوكيل"""
    agent = TodoAgent()
    
    print("=== وكيل قائمة المهام لمشروع Horus AI Pipeline ===")
    print("1. تحديث حالة مهمة")
    print("2. إضافة مهمة جديدة")
    print("3. إضافة قسم جديد")
    print("4. عرض حالة المشروع")
    print("5. البحث عن مهمة")
    print("6. حذف مهمة")
    print("7. تصدير قائمة المهام")
    print("8. خروج")
    
    while True:
        choice = input("\nاختر إجراءً (1-8): ")
        
        if choice == "1":
            task = input("أدخل نص المهمة: ")
            status = input("هل المهمة مكتملة؟ (نعم/لا): ").lower() in ["نعم", "y", "yes"]
            agent.update_task_status(task, status)
        
        elif choice == "2":
            task = input("أدخل نص المهمة: ")
            section = input("أدخل اسم القسم: ")
            status = input("هل المهمة مكتملة؟ (نعم/لا): ").lower() in ["نعم", "y", "yes"]
            agent.add_task(task, section, status)
        
        elif choice == "3":
            section = input("أدخل اسم القسم الجديد: ")
            agent.add_section(section)
        
        elif choice == "4":
            status = agent.get_project_status()
            print(f"\nحالة المشروع:")
            print(f"إجمالي المهام: {status['total_tasks']}")
            print(f"المهام المكتملة: {status['completed_tasks']}")
            print(f"نسبة الإكمال: {status['completion_percentage']:.2f}%")
            
            print("\nحالة الأقسام:")
            for section, stats in status["sections"].items():
                print(f"  {section}: {stats['completed']}/{stats['total']} ({stats['percentage']:.2f}%)")
        
        elif choice == "5":
            search_text = input("أدخل نص البحث: ")
            found_tasks = agent.search_task(search_text)
            if found_tasks:
                print("المهام التي تم العثور عليها:")
                for task in found_tasks:
                    print(f"  - {task}")
            else:
                print("لم يتم العثور على أي مهام.")
        
        elif choice == "6":
            task = input("أدخل نص المهمة لحذفها: ")
            success = agent.delete_task(task)
            if not success:
                print("لم يتم العثور على المهمة لحذفها.")
        
        elif choice == "7":
            export_file = input("أدخل اسم ملف التصدير (مثلاً export_tasks.txt): ")
            agent.export_tasks(export_file)
        
        elif choice == "8":
            break
        
        else:
            print("اختيار غير صالح. يرجى المحاولة مرة أخرى.")
    
    agent.close()
    print("\nشكراً لاستخدام وكيل قائمة المهام!")


if __name__ == "__main__":
    main()
