from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.query_params.query_params import parse_filters, parse_sort
from utils.query_params.dynamic_joins import DynamicJoinMixin
from utils.query_params.dynamic_pagination import DynamicPagination
from utils.query_params.open_api_params import paginated_parameters, list_parameters

from drf_spectacular.utils import extend_schema, extend_schema_view

from integrations.ollama.core import OllamaCore
from utils.transformers.json import extract_json, json_to_yaml


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
        print("Generating prompt...")
        prompt = self.ollama.generatePrompt(user_input, "complete-prompt.md")
        print("Calling Ollama...")
        result = self.ollama.call(prompt)
        print("\n--- Extracting JSON ---")
        json_output = extract_json(result)
        print("\nConverting JSON → YAML...")
        yaml_text = json_to_yaml(json_output)
        return Response(json_output)
