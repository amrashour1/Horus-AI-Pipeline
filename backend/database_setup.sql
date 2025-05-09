-- إنشاء قاعدة البيانات إذا لم تكن موجودة
CREATE DATABASE IF NOT EXISTS windsurf_pro_hours 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- استخدام قاعدة البيانات التي تم إنشاؤها
USE windsurf_pro_hours;

-- إنشاء جدول لتخزين معلومات الجلسات
CREATE TABLE IF NOT EXISTS sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,         -- معرّف فريد لكل جلسة (يزداد تلقائياً)
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- وقت بدء الجلسة (الافتراضي هو وقت الإنشاء)
    end_time TIMESTAMP NULL DEFAULT NULL,               -- وقت انتهاء الجلسة (يمكن أن يكون فارغاً إذا كانت الجلسة لا تزال نشطة)
    session_summary VARCHAR(255) NULL                    -- ملخص أو عنوان للجلسة (اختياري)
    -- يمكنك إضافة أعمدة أخرى هنا إذا احتجت، مثل user_id إذا كان لديك مستخدمين
);

-- إنشاء جدول لتخزين الرسائل داخل كل محادثة/جلسة
CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,         -- معرّف فريد لكل رسالة (يزداد تلقائياً)
    session_id INT NOT NULL,                           -- معرّف الجلسة التي تنتمي إليها هذه الرسالة
    sender VARCHAR(50) NOT NULL,                       -- مرسل الرسالة (مثلاً: 'user', 'ai', 'system')
    content TEXT NOT NULL,                             -- محتوى الرسالة النصي
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- وقت إرسال الرسالة (الافتراضي هو وقت الإنشاء)
    
    -- إنشاء مفتاح خارجي لربط الرسائل بالجلسات
    FOREIGN KEY (session_id) 
        REFERENCES sessions(session_id) 
        ON DELETE CASCADE -- إذا حُذفت جلسة، احذف كل رسائلها المرتبطة
        ON UPDATE CASCADE -- إذا تغير session_id (نادر الحدوث مع AUTO_INCREMENT)، قم بتحديثه هنا أيضاً
);

-- ملاحظة: يمكن إنشاء الفهارس لاحقاً باستخدام الأوامر التالية:
-- CREATE INDEX idx_session_id ON messages(session_id);
-- CREATE INDEX idx_sender ON messages(sender);
-- CREATE INDEX idx_session_start_time ON sessions(start_time);

-- رسالة تأكيد (اختياري)
SELECT 'قاعدة البيانات والجداول تم إنشاؤها بنجاح!' AS Status;
