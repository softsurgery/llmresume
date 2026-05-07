import json
import yaml

def extract_json(text: str) -> str:
    """
    Extract first JSON object from LLM output.
    Works even if model adds garbage before/after.
    """
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]

def fix_braces(text: str) -> str:
    """
    Auto-fix unbalanced braces in JSON.
    """
    open_braces = text.count("{")
    close_braces = text.count("}")
    open_brackets = text.count("[")
    close_brackets = text.count("]")
    
    fixed = text + ("}" * (open_braces - close_braces)) + ("]" * (open_brackets - close_brackets))
    return fixed

def json_to_yaml(json_input: str) -> str:
    # Fix braces first
    fixed_json = fix_braces(json_input)
    data = json.loads(fixed_json)
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True
    )