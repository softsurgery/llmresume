import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3:0.6b")

class OllamaCore:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent

    def call(self, prompt: str, timeout: int = 120):
        print(f"Connecting to Ollama at {OLLAMA_HOST}...")

        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )

        response.raise_for_status()
        return response.json()
    
    def generatePrompt(self, prompt: str, template: str, timeout: int = 120):
        template_path = self.base_dir / "templates" / template

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content.replace("{prompt}", prompt)
        