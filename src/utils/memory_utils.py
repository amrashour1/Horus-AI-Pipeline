import json
import os
from datetime import datetime
import logging

# سنستخدم تخزين بسيط قائم على الملفات للمرحلة الأولى
# يمكن ترقيته لاحقًا إلى Redis وChromaDB

class SimpleMemory:
    """
    ذاكرة بسيطة قائمة على الملفات للمرحلة الأولى من المشروع
    """
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()

    def _load_memory(self):
        """تحميل الذاكرة من الملف"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"خطأ في تحميل الذاكرة: {str(e)}")
                return {"conversations": [], "metadata": {}}
        else:
            return {"conversations": [], "metadata": {}}

    def _save_memory(self):
        """حفظ الذاكرة إلى الملف"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"خطأ في حفظ الذاكرة: {str(e)}")

    def add(self, documents, metadatas=None):
        """إضافة وثائق إلى الذاكرة"""
        if not metadatas:
            metadatas = [{"time": datetime.now().isoformat()} for _ in documents]

        for doc, meta in zip(documents, metadatas):
            self.memory["conversations"].append({
                "text": doc,
                "metadata": meta
            })

        self._save_memory()

    def query(self, query_texts, n_results=3):
        """
        بحث بسيط في الذاكرة (في المرحلة الأولى، سنعيد آخر n_results من المحادثات)
        """
        results = self.memory["conversations"][-n_results:] if self.memory["conversations"] else []
        return {
            "documents": [item["text"] for item in results],
            "metadatas": [item["metadata"] for item in results]
        }

# دوال التوافق مع الواجهة السابقة


def init_working_memory():
    """
    تهيئة الذاكرة العاملة (مبسطة للمرحلة الأولى)
    """
    return SimpleMemory(memory_file="working_memory.json")


def init_long_term_memory():
    """
    تهيئة الذاكرة طويلة المدى (مبسطة للمرحلة الأولى)
    """
    return SimpleMemory(memory_file="long_term_memory.json")


def context_reminder(query, chat_hist, long_mem=None):
    """
    استرجاع السياق من الذاكرة
    """
    # التعامل مع حالة عدم توفر الذاكرة
    if long_mem is None:
        return "لا توجد محادثات سابقة."

    results = long_mem.query(query_texts=[query], n_results=3)

    # بناء تذكير بسيط من السياق السابق
    recent_history = chat_hist[-3:] if chat_hist and len(chat_hist) > 0 else []
    reminder = (
        f"تذكير من المحادثات السابقة: {results['documents']} | "
        f"سياق حديث: {recent_history}"
    )

    return reminder
