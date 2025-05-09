from google.cloud import aiplatform
from config import GOOGLE_AI_CREDENTIALS
import logging

class VertexAIService:
    def __init__(self):
        self.project_id = GOOGLE_AI_CREDENTIALS['project_id']
        self.location = GOOGLE_AI_CREDENTIALS['location']
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options={
                'api_endpoint': f'{self.location}-aiplatform.googleapis.com'
            }
        )
        self.logger = logging.getLogger(__name__)

    from google.cloud import aiplatform

    class VertexAIService:
        def predict(self, endpoint_id, instances):
            # تنفيذ منطق التنبؤات
            try:
                endpoint = self.client.endpoint_path(
                    project=self.project_id,
                    location=self.location,
                    endpoint=endpoint_id
                )
                response = self.client.predict(
                    endpoint=endpoint,
                    instances=instances
                )
                self.logger.info(f'تنبؤ ناجح: {response.predictions}')
                return response
            except Exception as e:
                self.logger.error(f'خطأ في التنبؤ: {str(e)}')
                raise

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )