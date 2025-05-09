# ملفات Docker في مشروع Horus AI Pipeline

يحتوي هذا المجلد على جميع ملفات Docker المستخدمة في المشروع.

## التغييرات الحديثة

### تحسينات تم تنفيذها بتاريخ 2025-05-07:
1. **تحديث docker-compose.yml**:
   - إضافة خدمات Redis وMySQL
   - إعداد Health Checks للخدمات
   - إضافة volumes للبيانات المستمرة

2. **تحسين Dockerfile الرئيسي**:
   - استخدام multi-stage build
   - إضافة بيئة افتراضية لعزل الحزم
   - تثبيت curl لفحص الصحة

3. **إرشادات جديدة**:
   ```bash
   # لبدء جميع الخدمات مع المراقبة
   docker-compose up --build
   
   # لفحص حالة الخدمات
   docker-compose ps
   
   # لوقف الخدمات
   docker-compose down
   ```

## الهيكل الحالي للملفات

### ملفات التطوير
- `Dockerfile` - ملف Docker الرئيسي لبيئة التطوير
- `docker-compose.yml` - تكوين Docker Compose للتطوير المحلي
- `.dockerignore` - قائمة الملفات المستثناة من بناء Docker

### ملفات الاختبار
- `Dockerfile.test` - ملف Docker لبيئة الاختبار

### ملفات النشر
- `deploy/Dockerfile` - ملف Docker للنشر في بيئة الإنتاج

## الاستخدام

### تشغيل بيئة التطوير
```bash
docker-compose up
```

### تشغيل الاختبارات
```bash
docker build -f Dockerfile.test -t horus-test .
docker run horus-test
```

### بناء صورة الإنتاج
```bash
docker build -f deploy/Dockerfile -t horus-prod .
```