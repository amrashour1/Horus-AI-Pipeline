import tkinter as tk

class TodoUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("واجهة قائمة المهام")
        self.root.geometry("400x300")
        
        # إنشاء عناصر الواجهة
        self.task_entry = tk.Entry(self.root, width=30)
        self.task_entry.pack(pady=10)
        
        self.add_button = tk.Button(self.root, text="إضافة مهمة", command=self.add_task)
        self.add_button.pack(pady=5)
        
        self.task_list = tk.Listbox(self.root, width=50)
        self.task_list.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.root.mainloop()
    
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = TodoUI()