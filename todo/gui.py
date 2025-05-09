import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from config import DB_CONFIG, GOOGLE_AI_CREDENTIALS, CLOUD_LOGGING_CONFIG
from services.vertex_ai_service import VertexAIService
import logging

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام قائمة المهام الذكي")
        self.root.geometry("800x600")
        
        # تكوين قاعدة البيانات
        self.db = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.db.cursor()
        
        # تهيئة خدمات الذكاء الاصطناعي
        self.ai_service = VertexAIService()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(CLOUD_LOGGING_CONFIG['log_level'])
        
        # إنشاء الواجهة
        self.create_widgets()
    
    def create_widgets(self):
        # إطار رئيسي
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # عنوان
        title_label = ttk.Label(main_frame, text="نظام قائمة المهام الذكي", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # إضافة مهمة جديدة
        task_frame = ttk.LabelFrame(main_frame, text="إضافة مهمة جديدة", padding="5")
        task_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(task_frame, text="عنوان المهمة:").grid(row=0, column=0, padx=5)
        self.task_entry = ttk.Entry(task_frame, width=50)
        self.task_entry.bind('<KeyRelease>', self.suggest_tasks)
        self.task_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(task_frame, text="إضافة", command=self.add_task).grid(row=0, column=2, padx=5)
        
        # قائمة المهام
        tasks_frame = ttk.LabelFrame(main_frame, text="قائمة المهام", padding="5")
        tasks_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # عرض المهام
        self.tasks_tree = ttk.Treeview(tasks_frame, columns=("id", "task", "status"), show="headings")
        self.tasks_tree.heading("id", text="الرقم")
        self.tasks_tree.heading("task", text="المهمة")
        self.tasks_tree.heading("status", text="الحالة")
        
        self.tasks_tree.column("id", width=50)
        self.tasks_tree.column("task", width=400)
        self.tasks_tree.column("status", width=100)
        
        self.tasks_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        # أزرار التحكم
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(control_frame, text="تحديث الحالة", command=self.toggle_status).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="حذف المهمة", command=self.delete_task).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="تحديث القائمة", command=self.refresh_tasks).grid(row=0, column=2, padx=5)
        
        # تحميل المهام
        self.refresh_tasks()
    
    def suggest_tasks(self, event):
        # نظام الاقتراحات الذكية
        predictions = self.ai_service.predict(
            endpoint_id='TODO_MODEL_ENDPOINT',
            instances=[{'text': partial_task}]
        )
        self.show_suggestions(predictions)
        self.logger.info(f'تم توليد اقتراحات للمهمة: {partial_task}')
    except Exception as e:
        self.logger.error(f'خطأ في توليد الاقتراحات: {str(e)}')

    def show_suggestions(self, predictions):
        """عرض الاقتراحات في قائمة منبثقة"""
        # تنفيذ منطق عرض الاقتراحات هنا
        pass

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            try:
                self.cursor.execute("INSERT INTO tasks (task_name, status) VALUES (%s, %s)", (task, 0))
                self.db.commit()
                self.task_entry.delete(0, tk.END)
                self.refresh_tasks()
                messagebox.showinfo("نجاح", "تمت إضافة المهمة بنجاح")
            except:
                messagebox.showerror("خطأ", "حدث خطأ أثناء إضافة المهمة")
        else:
            messagebox.showwarning("تنبيه", "الرجاء إدخال عنوان المهمة")
    
    def toggle_status(self):
        selection = self.tasks_tree.selection()
        if selection:
            item = self.tasks_tree.item(selection[0])
            task_id = item['values'][0]
            try:
                self.cursor.execute("UPDATE tasks SET status = NOT status WHERE id = %s", (task_id,))
                self.db.commit()
                self.refresh_tasks()
            except:
                messagebox.showerror("خطأ", "حدث خطأ أثناء تحديث حالة المهمة")
        else:
            messagebox.showwarning("تنبيه", "الرجاء اختيار مهمة")
    
    def delete_task(self):
        selection = self.tasks_tree.selection()
        if selection:
            if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف المهمة المحددة؟"):
                item = self.tasks_tree.item(selection[0])
                task_id = item['values'][0]
                try:
                    self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                    self.db.commit()
                    self.refresh_tasks()
                    messagebox.showinfo("نجاح", "تم حذف المهمة بنجاح")
                except:
                    messagebox.showerror("خطأ", "حدث خطأ أثناء حذف المهمة")
        else:
            messagebox.showwarning("تنبيه", "الرجاء اختيار مهمة")
    
    def refresh_tasks(self):
        # مسح القائمة الحالية
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        # تحميل المهام من قاعدة البيانات
        try:
            self.cursor.execute("SELECT id, task_name, status FROM tasks ORDER BY id")
            for task in self.cursor.fetchall():
                status = "مكتملة" if task[2] else "قيد التنفيذ"
                self.tasks_tree.insert("", tk.END, values=(task[0], task[1], status))
        except:
            messagebox.showerror("خطأ", "حدث خطأ أثناء تحميل المهام")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()