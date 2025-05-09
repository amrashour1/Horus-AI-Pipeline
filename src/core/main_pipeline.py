
from vertex_utils import init_vertex, deploy_model, call_gemini
from memory_utils import init_working_memory, init_long_term_memory, context_reminder
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# الإعداد
PROJECT_ID = "YOUR_PROJECT_ID"
LOCATION = "us-central1"
CREDENTIALS_PATH = "path/to/key.json"
IMAGE_URI = "us-docker.pkg.dev/vertex-ai/prediction/gemini-2.5-flash:latest"

init_vertex(PROJECT_ID, LOCATION, CREDENTIALS_PATH)
endpoint = deploy_model("gemini-2.5-flash", IMAGE_URI)
working_mem = init_working_memory("REDIS_HOST")
long_mem = init_long_term_memory()

def deep_analysis(text):
    return call_gemini(endpoint, f"تحليل فلسفي: {text}")

def logical_analysis(text):
    return call_gemini(endpoint, f"تحليل منطقي: {text}")

def run_parallel(functions):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fn) for fn in functions]
        return [f.result() for f in futures]

# مدخل المستخدم من الواجهة
user_input = "النص المُدخل من المستخدم"
chat_history = ["تفاعل سابق 1", "تفاعل سابق 2", "تفاعل سابق 3"]

reminder = context_reminder(user_input, chat_history, long_mem, working_mem)
analyses = run_parallel([
    lambda: deep_analysis(reminder + user_input),
    lambda: logical_analysis(reminder + user_input),
])

# استخدم GPT4All أو أي مرحلة تنسيق أخرى هنا
def call_gpt4all(analyses):
    return f"النتيجة النهائية:
{analyses[0]}

{analyses[1]}"

final_output = call_gpt4all(analyses)
long_mem.add(documents=[user_input], metadatas=[{"time": str(datetime.now())}])
print(final_output)
