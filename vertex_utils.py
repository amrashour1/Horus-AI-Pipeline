
from google.cloud import aiplatform

def init_vertex(project_id, location, credentials_path):
    aiplatform.init(
        project=project_id,
        location=location,
        credentials=credentials_path,
    )

def deploy_model(display_name, image_uri, machine_type="n1-standard-4"):
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
    response = endpoint.predict(instances=[{"content": prompt}])
    return response.predictions[0]["content"]
