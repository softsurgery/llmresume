import uuid
import os
from pathlib import Path

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.conf import settings

from utils.query_params.query_params import parse_filters, parse_sort
from utils.query_params.dynamic_joins import DynamicJoinMixin
from utils.query_params.dynamic_pagination import DynamicPagination
from utils.query_params.open_api_params import paginated_parameters, list_parameters

from drf_spectacular.utils import extend_schema, extend_schema_view

from integrations.ollama.core import OllamaCore
from utils.transformers.json import extract_json, json_to_yaml
from utils.rendercv.functions import run_rendercv


@extend_schema_view(
    create=extend_schema(
        summary="create cv",
        description="create cv from user input",
        tags=["Resume"]
    )
)
class ResumeViewset(DynamicJoinMixin, viewsets.ViewSet):
    ollama = OllamaCore()
    
    def create(self, request):
        user_input = request.data.get("prompt")
        if not user_input:
            return Response({"error": "prompt field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(f"Enhancing prompt")
            prompt = self.ollama.generatePrompt(user_input, "rephrase-enhance.md")
            print("Calling Ollama...")
            result = self.ollama.call(prompt)
            print(f"Prompt enhanced: {result}")
            print("Generating prompt...")
            prompt = self.ollama.generatePrompt(result.get("response", ""), "complete-prompt.md")
            print("Calling Ollama...")
            result = self.ollama.call(prompt)
            
            print("\n--- Extracting JSON ---")
            raw_response = result.get("response", "")
            json_output = extract_json(raw_response)
            
            print("\nConverting JSON → YAML...")
            yaml_text = json_to_yaml(json_output)

            # Save YAML and render CV
            job_id = str(uuid.uuid4())
            job_dir = Path(settings.MEDIA_ROOT) / "jobs" / job_id
            job_dir.mkdir(parents=True, exist_ok=True)

            yaml_path = job_dir / "cv.yaml"
            yaml_path.write_text(yaml_text, encoding="utf-8")

            # Run RenderCV to generate output files
            run_rendercv(str(yaml_path), str(job_dir))

            return Response({"job_id": job_id, "message": "CV generated successfully"})
        except Exception as e:
            print(f"Error generating CV: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
