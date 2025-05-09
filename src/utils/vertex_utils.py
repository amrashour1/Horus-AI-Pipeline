
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

def init_vertex(project_id, location, credentials_path=None):
    """
    تهيئة Vertex AI مع إمكانية استخدام الاعتمادات الافتراضية
    """
    if credentials_path and os.path.exists(credentials_path):
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(credentials_path)

        aiplatform.init(
            project=project_id,
            location=location,
            credentials=credentials,
        )

        # تهيئة Vertex AI للنماذج التوليدية
        vertexai.init(project=project_id, location=location, credentials=credentials)
    else:
        # استخدام الاعتمادات الافتراضية (مناسب لبيئة Google Cloud)
        aiplatform.init(
            project=project_id,
            location=location,
        )

        # تهيئة Vertex AI للنماذج التوليدية
        vertexai.init(project=project_id, location=location)

def get_gemini_model(model_name="gemini-1.5-flash"):
    """
    الحصول على نموذج Gemini من Model Garden
    """
    return GenerativeModel(model_name)

def call_gemini_direct(model, prompt, temperature=0.7, max_output_tokens=1024):
    """
    استدعاء نموذج Gemini مباشرة (بدون نشر نقطة نهاية)
    """
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }
    )
    return response.text

def call_gemini_multimodal(model, text_prompt, image_data=None):
    """
    استدعاء نموذج Gemini مع دعم الصور (إذا كان النموذج يدعم ذلك)
    """
    if image_data:
        response = model.generate_content([text_prompt, Part.from_data(image_data, "image/jpeg")])
    else:
        response = model.generate_content(text_prompt)
    return response.text

# الدوال القديمة للتوافق مع الكود الحالي
def deploy_model(display_name, image_uri, machine_type="n1-standard-4"):
    """
    نشر نموذج كنقطة نهاية (للنماذج المخصصة)
    """
    model = aiplatform.Model.upload(
        display_name=display_name,
        serving_container_image_uri=image_uri,
    )
    endpoint = model.deploy(
        machine_type=machine_type,
        min_replica_count=1,
        max_replica_count=2,
        traffic_split={"0": 100},
    )
    return endpoint

def call_gemini(endpoint, prompt):
    """
    استدعاء نموذج من خلال نقطة نهاية
    """
    response = endpoint.predict(instances=[{"content": prompt}])
    return response.predictions[0]["content"]
