import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:0.6b")

class OllamaError(Exception):
    pass

class TemplateError(Exception):
    pass

class OllamaCore:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent

        self.session = requests.Session()

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def call(
        self,
        prompt: str,
        timeout: int = 120,
        temperature: float = 0.7,
        format_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        logger.info("Sending request to Ollama")

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if format_schema:
            payload["format"] = format_schema

        try:
            response = self.session.post(
                f"{OLLAMA_HOST}/api/generate",
                json=payload,
                timeout=timeout
            )

            response.raise_for_status()

            data = response.json()

            logger.info("Response received successfully")

            return data

        except requests.Timeout as e:
            logger.exception("Ollama request timed out")
            raise OllamaError("Request timed out") from e

        except requests.RequestException as e:
            logger.exception("Ollama request failed")
            raise OllamaError(str(e)) from e

    def generate_json(
        self,
        prompt: str,
        schema_model: type[BaseModel],
        timeout: int = 120
    ) -> BaseModel:

        schema = schema_model.model_json_schema()

        response = self.call(
            prompt=prompt,
            timeout=timeout,
            format_schema=schema
        )

        raw = response.get("response", "")

        try:
            parsed = json.loads(raw)
            validated = schema_model.model_validate(parsed)

            logger.info("JSON validated successfully")

            return validated

        except (json.JSONDecodeError, ValidationError) as e:
            logger.exception("Failed to validate model output")
            raise OllamaError(f"Invalid structured output: {e}") from e

    def generate_prompt(
        self,
        prompt: str,
        template: str
    ) -> str:

        template_path = self.base_dir / "templates" / template

        if not template_path.exists():
            logger.error(f"Template not found: {template_path}")
            raise TemplateError(f"Template not found: {template_path}")

        try:
            content = template_path.read_text(encoding="utf-8")

            logger.debug(f"Loaded template: {template}")

            return content.replace("{prompt}", prompt)

        except Exception as e:
            logger.exception("Failed to load template")
            raise TemplateError(str(e)) from e

    def health(self) -> bool:
        try:
            response = self.session.get(
                f"{OLLAMA_HOST}/api/tags",
                timeout=5
            )

            response.raise_for_status()

            return True

        except Exception:
            return False