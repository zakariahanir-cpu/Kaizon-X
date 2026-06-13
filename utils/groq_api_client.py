import os
import requests
import json

class GroqClient:
    def __init__(self, api_key=None, model="llama-3.1-70b-versatile"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model

    def chat(self, messages, temperature=0.7, max_tokens=4096):
        if not self.api_key:
            # In a real scenario, we'd need a key. For now, we'll simulate or assume it's in env.
            # If not found, we'll return a placeholder for development.
            return "Error: Groq API key is missing. Please set the GROQ_API_KEY environment variable."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error communicating with Groq: {str(e)}"
