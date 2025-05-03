from memgpt import Agent
import redis
import chromadb

def init_working_memory(redis_host="localhost", port=6379):
    r = redis.Redis(host=redis_host, port=port)
    agent = Agent(
        persona="assistant",
        memory_backend=r,
        interface="api"
    )
    return agent

def init_long_term_memory():
    client = chromadb.Client()
    return client.create_collection("chat_history", embedding_function="embedding-model")

def context_reminder(query, chat_hist, long_mem, working_mem):
    results = long_mem.query(query_texts=[query], n_results=3)
    reminder = working_mem.generate(
        f"تذكير: {results['documents']} | سياق سابق: {chat_hist[-3:]}"
    )
    return reminder
