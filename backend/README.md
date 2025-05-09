# قاعدة بيانات مشروع Horus AI Pipeline

هذا المستند يشرح هيكل قاعدة البيانات المستخدمة في مشروع Horus AI Pipeline وكيفية استخدامها.

## هيكل قاعدة البيانات

تتكون قاعدة البيانات من الجداول التالية:

### جدول `sessions`

يستخدم لتخزين معلومات الجلسات:

| العمود | النوع | الوصف |
|--------|------|-------|
| `session_id` | INT AUTO_INCREMENT | معرّف فريد لكل جلسة (المفتاح الأساسي) |
| `start_time` | TIMESTAMP | وقت بدء الجلسة (الافتراضي هو وقت الإنشاء) |
| `end_time` | TIMESTAMP | وقت انتهاء الجلسة (يمكن أن يكون فارغاً إذا كانت الجلسة لا تزال نشطة) |
| `session_summary` | VARCHAR(255) | ملخص أو عنوان للجلسة (اختياري) |

### جدول `messages`

يستخدم لتخزين الرسائل داخل كل محادثة/جلسة:

| العمود | النوع | الوصف |
|--------|------|-------|
| `message_id` | INT AUTO_INCREMENT | معرّف فريد لكل رسالة (المفتاح الأساسي) |
| `session_id` | INT | معرّف الجلسة التي تنتمي إليها هذه الرسالة (مفتاح خارجي) |
| `sender` | VARCHAR(50) | مرسل الرسالة (مثلاً: 'user', 'ai', 'system') |
| `content` | TEXT | محتوى الرسالة النصي |
| `timestamp` | TIMESTAMP | وقت إرسال الرسالة (الافتراضي هو وقت الإنشاء) |

## الفهارس

تم إنشاء الفهارس التالية لتحسين أداء الاستعلامات:

- `idx_session_id` على عمود `session_id` في جدول `messages`
- `idx_sender` على عمود `sender` في جدول `messages`
- `idx_session_start_time` على عمود `start_time` في جدول `sessions`

## كيفية الإعداد

1. تأكد من تثبيت MySQL على نظامك
2. قم بتعديل ملف `db_config.py` لتعيين إعدادات الاتصال الصحيحة
3. قم بتشغيل سكريبت `setup_database.py` لإنشاء قاعدة البيانات والجداول:

```bash
python setup_database.py
```

## استخدام مدير قاعدة البيانات

يمكنك استخدام الفئة `DatabaseManager` الموجودة في `db_manager.py` للتفاعل مع قاعدة البيانات. فيما يلي بعض الأمثلة:

### إنشاء جلسة جديدة

```python
from db_manager import DatabaseManager

db = DatabaseManager()
session_id = db.create_session("جلسة تجريبية")
print(f"تم إنشاء جلسة جديدة بمعرف: {session_id}")
```

### إضافة رسائل إلى جلسة

```python
db.add_message(session_id, "user", "مرحباً! كيف يمكنني استخدام النظام؟")
db.add_message(session_id, "ai", "مرحباً بك! يمكنك استخدام النظام للتفاعل مع نماذج الذكاء الاصطناعي المختلفة.")
```

### الحصول على رسائل الجلسة

```python
messages = db.get_session_messages(session_id)
for msg in messages:
    print(f"{msg['sender']}: {msg['content']}")
```

### إنهاء جلسة

```python
db.end_session(session_id)
print(f"تم إنهاء الجلسة {session_id}")
```

## ملاحظات هامة

- يتم استخدام ترميز `utf8mb4` لدعم اللغة العربية والرموز التعبيرية
- يتم تنفيذ العمليات تلقائياً (`autocommit=True`)
- يستخدم النظام تجمع اتصالات لتحسين الأداء
- يتم تسجيل جميع العمليات في ملف `database.log`

## متطلبات النظام

- Python 3.6 أو أحدث
- MySQL 5.7 أو أحدث
- حزمة `mysql-connector-python`

يمكنك تثبيت المتطلبات باستخدام:

```bash
pip install mysql-connector-python
```
