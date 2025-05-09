# مشروع Horus AI Pipeline

<div dir="rtl">

هذا المشروع يقدم خط أنابيب ذكاء اصطناعي متكامل باستخدام Google Cloud Vertex AI وGemini لتحليل النصوص وتوفير تحليلات متعددة الأبعاد. يمكن استخدامه لمعالجة البيانات النصية وتحليلها واستخراج الرؤى منها بشكل آلي.

## نظرة عامة

يستخدم مشروع Horus AI Pipeline نماذج الذكاء الاصطناعي المتقدمة من Google Cloud Vertex AI وGemini لتوفير القدرات التالية:

- تحليل النصوص ومعالجتها بلغات متعددة
- استخراج المعلومات والكيانات المهمة من النصوص
- توليد تقارير تحليلية متعددة الأبعاد
- إدارة الذاكرة العاملة وطويلة المدى للمحادثات
- واجهة برمجة تطبيقات (API) سهلة الاستخدام للتكامل مع تطبيقات أخرى

## تحديث: خطة التنفيذ المتطورة

تم تطوير خطة المشروع لتشمل نماذج ذكاء اصطناعي متعددة ومتقدمة. للاطلاع على الخطة الكاملة، راجع [خطة المشروع التفصيلية](PROJECT_PLAN.md). النظام الجديد يتضمن:

### النماذج المتكاملة للذكاء الاصطناعي
- **Gemini 1.5/2.5 Flash**: المعالجة العامة وتوليد الاستجابات
- **DeepSeekR1**: التحليل الرياضي والمنطقي
- **Claude 3.7 Sonnet**: تحليل القضايا الفلسفية والأخلاقية
- **GPT-4**: توليد المحتوى الإبداعي والتفاعلي

### مراحل التنفيذ

1. **المرحلة الحالية**: نموذج Gemini 1.5 Flash مع ذاكرة بسيطة
   - استخدام نموذج Gemini 1.5 Flash من Google AI
   - تنفيذ نظام ذاكرة بسيط قائم على الملفات
   - واجهة سطر أوامر بسيطة للتفاعل مع النموذج

2. **المرحلة التالية**: النظام المتكامل متعدد النماذج
   - دمج نماذج الذكاء الاصطناعي المتعددة
   - تنفيذ نظام RAG مع ChromaDB وVertex Matching Engine
   - إضافة واجهة API متقدمة للتكامل مع التطبيقات الأخرى
   - إضافة نظام Web Scraping لجمع البيانات

## المتطلبات الأساسية

1. حساب Google Cloud Platform مع تفعيل الفوترة
2. تثبيت [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. **جديد**: مفتاح API من [Google AI Studio](https://makersuite.google.com/app/apikey) (للطريقة الموصى بها)
4. Python 3.8 أو أحدث
5. حساب Redis (اختياري، للذاكرة المتقدمة)

## خطوات الإعداد

### 1. تفعيل Google Cloud APIs

## إعداد بيئة Google Cloud

لتفعيل جميع واجهات برمجة التطبيقات المطلوبة للمشروع دفعة واحدة، تأكد أولاً أن المشروع النشط هو الصحيح باستخدام الأمر:

```bash
gcloud config set project PROJECT_ID
```

ثم نفذ الأمر التالي:

```bash
gcloud services enable aiplatform.googleapis.com storage.googleapis.com iam.googleapis.com run.googleapis.com appengine.googleapis.com
```

### 2. إنشاء حساب خدمة وتوليد مفتاح JSON

1. انتقل إلى [Google Cloud Console](https://console.cloud.google.com/)
2. اذهب إلى IAM & Admin > Service Accounts
3. انقر على "Create Service Account"
4. أدخل اسم حساب الخدمة ووصفه
5. امنح الأذونات التالية:
   - Vertex AI User
   - Storage Admin
   - Vertex AI Administrator (إذا كنت ستقوم بإنشاء نماذج مخصصة)
6. انقر على "Create Key" واختر JSON
7. احفظ الملف في مجلد المشروع

### 3. إعداد بيئة التطوير

1. استنساخ المستودع:

```bash
git clone https://github.com/your-username/horus-ai-pipeline.git
cd horus-ai-pipeline
```

2. إنشاء بيئة Python افتراضية:

```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
venv\Scripts\activate  # على Windows
```

3. تثبيت المكتبات المطلوبة:

```bash
pip install -r requirements.txt
```

### 4. تكوين متغيرات البيئة

قم بإنشاء ملف `.env` بناءً على نموذج `.env.example` وأضف المعلومات الخاصة بمشروعك:

```env
PROJECT_ID=your-project-id
REGION=us-central1
KEY_PATH=path/to/your-key.json
GEMINI_API_KEY=your-gemini-api-key  # مفتاح API من Google AI Studio
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password  # إذا كان مطلوبًا
MODEL_NAME=gemini-1.5-flash  # أو أي نموذج آخر تفضله
```

## تشغيل المشروع

### الجزء الأول: نموذج Gemini

#### باستخدام Google AI Studio (الموصى به)

```bash
python app_gemini.py
```

#### باستخدام Vertex AI

```bash
python app.py
```

### الجزء الثاني: النظام المتكامل متعدد النماذج

```bash
# تشغيل النظام المتكامل
python orchestrator.py

# تشغيل واجهة API
python api.py
```

### استخدام واجهة API

يمكنك تشغيل خادم API المحلي باستخدام:

```bash
python -m flask run --host=0.0.0.0 --port=8080
```

ثم يمكنك إرسال طلبات POST إلى `http://localhost:8080/analyze` مع JSON يحتوي على النص المراد تحليله.

## نشر المشروع على Google Cloud

### باستخدام Cloud Run

1. بناء صورة Docker:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/horus-ai
```

2. نشر الخدمة:

```bash
gcloud run deploy horus-ai --image gcr.io/PROJECT_ID/horus-ai --platform managed --allow-unauthenticated
```

### باستخدام App Engine

1. تأكد من وجود ملف `app.yaml` في المجلد بالمحتوى التالي:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

env_variables:
  PROJECT_ID: "your-project-id"
  REGION: "us-central1"
```

2. قم بالنشر:

```bash
gcloud app deploy
```

### باستخدام Vertex AI Endpoints

لنشر النموذج كنقطة نهاية Vertex AI:

```bash
python deploy_vertex_endpoint.py
```

## نشر وتكامل نماذج Gemini المتقدمة

### نشر نموذج Gemini 2.5 Flash من Model Garden

يمكنك نشر أحدث نماذج Gemini مباشرة من Model Garden على Vertex AI باتباع الخطوات التالية:

#### 1. تهيئة العميل

```python
from google.cloud import aiplatform

# تهيئة العميل
aiplatform.init(
    project="YOUR_PROJECT_ID",
    location="us-central1",            # اختَر أقرب منطقة
    credentials="path/to/key.json",
)
```

#### 2. تعيين النموذج من Model Garden

```python
# تعيين النموذج من Model Garden
model = aiplatform.Model.upload(
    display_name="gemini-2.5-flash",
    serving_container_image_uri=(
      "us-docker.pkg.dev/vertex-ai/prediction/gemini-2.5-flash:latest"
    )
)
```

#### 3. إنشاء Endpoint

```python
# إنشاء Endpoint
endpoint = model.deploy(
    machine_type="n1-standard-4",      # أو اختر أقل حسب الحجم
    min_replica_count=1,
    max_replica_count=2,
    traffic_split={"0": 100},
)
```

### استدعاء النموذج من طبقة المعالجة

#### وظيفة استدعاء النموذج

```python
def call_gemini(endpoint: aiplatform.Endpoint, prompt: str) -> str:
    response = endpoint.predict(instances=[{"content": prompt}])
    return response.predictions[0]["content"]
```

#### دمجه في Pipeline متعدد الوكلاء

```python
from concurrent.futures import ThreadPoolExecutor

def deep_analysis(text):
    return call_gemini(endpoint, f"تحليل فلسفي: {text}")

def logical_analysis(text):
    return call_gemini(endpoint, f"تحليل منطقي: {text}")

# تنفيذ متوازٍ
with ThreadPoolExecutor() as ex:
    fa = ex.submit(deep_analysis, user_input)
    fb = ex.submit(logical_analysis, user_input)
    analyses = {"deep": fa.result(), "logical": fb.result()}
```

### تركيب نظام الذاكرة المتقدم

#### ذاكرة عاملة (MemGPT + Redis)

```python
from memgpt import Agent
import redis

r = redis.Redis(host="REDIS_HOST", port=6379)
working_mem = Agent(
    persona="assistant",
    memory_backend=r,        # يعبّر عن التخزين الفوري
    interface="api"
)
```

#### ذاكرة طويلة الأمد (ChromaDB)

```python
import chromadb

client = chromadb.Client()
long_mem = client.create_collection("chat_history", embedding_function="embedding-model")
```

#### آلية التذكير الذكي

```python
def context_reminder(query, chat_hist):
    # استرجاع من ChromaDB
    results = long_mem.query(query_texts=[query], n_results=3)
    reminder = working_mem.generate(
        f"تذكير: {results['documents']} | سياق سابق: {chat_hist[-3:]}"
    )
    return reminder
```

### Workflow كامل

فيما يلي مثال لتدفق العمل الكامل الذي يجمع بين نماذج Gemini المتقدمة وآليات الذاكرة:

```python
# مثال تجريبي
user_input = UITARS.capture_input()
reminder = context_reminder(user_input, chat_history)
analyses = run_parallel([
    lambda: deep_analysis(reminder + user_input),
    lambda: logical_analysis(reminder + user_input),
])
final = call_gpt4all(analyses)
long_mem.add(documents=[user_input], metadatas=[{"time": now()}])
return final
```

### مراقبة الأداء وضبط التكلفة

لضمان كفاءة التشغيل وضبط التكاليف، يمكنك اتباع الإرشادات التالية:

- **Cloud Monitoring**: استخدم Metrics لمراقبة استهلاك CPU/Memory وLatency
- **Budget Alerts**: حدد إنذارات إنفاق شهرية لتجنب التكاليف غير المتوقعة
- **Scaling**: اضبط `min_replica_count` و`max_replica_count` حسب حجم الزيارات المتوقع

```python
# مثال لضبط التكلفة عن طريق تعديل إعدادات النشر
endpoint = model.deploy(
    machine_type="n1-standard-2",      # خفض حجم الآلة لتقليل التكلفة
    min_replica_count=1,              # الحد الأدنى من النسخ
    max_replica_count=5,              # زيادة الحد الأقصى للتعامل مع ذروة الاستخدام
    traffic_split={"0": 100},
)
```

## هيكل المشروع

- `horus_ai_pipeline.py`: الملف الرئيسي للمشروع
- `vertex_utils.py`: وظائف مساعدة للتفاعل مع Vertex AI
- `memory_utils.py`: وظائف إدارة الذاكرة العاملة وطويلة المدى
- `main_pipeline.py`: نسخة بديلة من خط الأنابيب
- `requirements.txt`: قائمة المكتبات المطلوبة
- `Dockerfile`: ملف لبناء صورة Docker
- `app.yaml`: ملف تكوين App Engine
- `deploy_vertex_endpoint.py`: سكريبت لنشر نقطة نهاية Vertex AI
- `.env.example`: نموذج لملف متغيرات البيئة

## استخدامات متقدمة

### تخصيص النماذج

يمكنك تخصيص النماذج المستخدمة عن طريق تعديل المتغير `MODEL_NAME` في ملف `.env` أو مباشرة في الكود:

```python
model_name = "gemini-1.0-pro-vision"  # لدعم تحليل الصور
```

### تكامل Redis للذاكرة

لتفعيل ذاكرة طويلة المدى باستخدام Redis:

```python
from memory_utils import RedisMemory

memory = RedisMemory(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
pipeline = HorusAIPipeline(memory=memory)
```

## التحديثات الأخيرة

### تحديث 2025-05-04

- **إضافة دعم Google AI Studio**: تم إضافة ملف `gemini_utils.py` و `app_gemini.py` لدعم استخدام Google AI Studio بدلاً من Vertex AI، مما يسهل الاستخدام ويقلل من متطلبات الصلاحيات.
- **تحسين إدارة الذاكرة**: تم تحسين نظام الذاكرة في `memory_utils.py` للتعامل مع حالات عدم توفر الذاكرة.
- **إصلاح مشكلات الاعتماد**: تم إصلاح مشكلات في تهيئة Vertex AI وإدارة الاعتمادات في `vertex_utils.py`.
- **تحديث المكتبات**: تم تحديث قائمة المكتبات المطلوبة في `requirements.txt` لتشمل المكتبات الضرورية مثل `google-generativeai`.

## استكشاف الأخطاء وإصلاحها

### مشاكل الاتصال بـ Google Cloud

- تأكد من صحة مفتاح JSON وأذونات حساب الخدمة
- تحقق من تفعيل واجهات برمجة التطبيقات المطلوبة
- استخدم `gcloud auth application-default login` للتحقق من صحة الاعتماد

### أخطاء النموذج

- تأكد من استخدام اسم نموذج صحيح ومدعوم في منطقتك
- تحقق من حدود الاستخدام والكوتا في مشروع Google Cloud الخاص بك
- **جديد**: إذا واجهت مشكلة "Permission denied" مع Vertex AI، جرب استخدام Google AI Studio بدلاً من ذلك عن طريق تشغيل `app_gemini.py`

## المساهمة

nنرحب بمساهماتكم! يرجى اتباع هذه الخطوات:

1. افتح issue لمناقشة التغيير المقترح
2. قم بعمل fork للمستودع
3. أنشئ فرعًا جديدًا لميزتك
4. أرسل طلب سحب (Pull Request)

## الترخيص

هذا المشروع مرخص بموجب [MIT License](LICENSE).

</div>