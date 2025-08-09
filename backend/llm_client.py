import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

class LLMClient:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or MODEL
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment.")

    def ask(self, prompt, context=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        system_prompt = (
            "You are a helpful assistant. Answer the user's question strictly using ONLY the information in the provided context. "
            "If the answer is not present in the context, reply: 'Sorry, the answer to your question is not found in the provided document.'\n\n"
            f"Context:\n{context or '[No context provided]'}"
        )
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"]

llm_client = LLMClient()
