import os
import requests
import yaml
import json
import subprocess
import sys
from dotenv import load_dotenv

# ================= CONFIG =================

load_dotenv()

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3:0.6b")

OUTPUT_YAML = "cv_output.yaml"
RENDER_DIR = "rendercv_output"
PROMPT_TEMPLATE_FILE = "complete-prompt.md"

USER_INPUT = """
Manar – Interior Architect | Global Experience
Born: 2000 | Location: Madrid, Spain
Email: manar@example.com
 | Website: https://manar-design.com
 | LinkedIn: manar

Summary

Passionate interior architect with over 5 years of experience in global residential, commercial, and cultural projects. Skilled in blending sustainability, innovation, and cultural sensitivity in design solutions. Expert in 3D modeling, parametric design, furniture design, and adaptive reuse. Experienced collaborating with multinational teams to deliver high-quality, award-winning projects across Europe, North Africa, and Asia.

Education

Politecnico di Milano, Italy — Master’s in Interior Architecture (2022–2024)
Focus: Sustainable design, adaptive reuse, advanced 3D modeling, parametric design, material research.

Thesis: “Adaptive Living: Sustainable Interiors for High-Density Urban Housing”

Exchange semester: University of Tokyo, Japan (2023) — Research on compact multifunctional living solutions

University of Madrid, Spain — Bachelor’s in Architecture (2018–2022)

GPA: 3.9/4.0

Key Courses: Sustainable Architecture, Lighting Design, Urban Planning, Heritage Restoration

Professional Experience

Studio Forma, Barcelona, Spain — Junior Interior Architect (2022–2023)

Led a team of 4 designers for residential and boutique commercial interiors.

Designed sustainable furniture systems and optimized layouts with BIM and AutoCAD.

Managed client meetings, contractors, and material procurement to deliver projects on schedule.

Key projects:

Luxury apartment renovation in Eixample, Barcelona

Boutique co-working space with modular interiors

ArchiVision, Milan, Italy — Interior Design Intern (2021–2022)

Assisted in large-scale office and cultural center designs.

Produced 3D visualizations, material boards, and detailed renderings for client presentations.

Participated in international architectural competitions, including Milan Design Week 2022 submissions.

Freelance Interior Designer (2019–Present)

Completed 30+ projects in Spain, Italy, Morocco, UAE, and France.

Delivered luxury villas, eco-friendly apartments, boutique hotels, coworking spaces, and heritage building restorations.

Integrated smart home systems, modular furniture, and sustainable materials in designs.

Projects:

Eco-residential complex in Marrakech, Morocco

Smart minimalist apartment in Dubai, UAE

Co-living space in Valencia, Spain

Atelier Lumière, Paris, France — Design Research Fellow (2020–2021) (Imaginary but realistic)

Conducted research on light and spatial perception in urban apartments.

Developed modular furniture adaptable to compact spaces.

Published paper: “Urban Minimalism and Sustainable Living Spaces” at the European Interior Architecture Conference.

Global Habitat Institute, Tokyo, Japan — Visiting Designer (2019) (Imaginary but realistic)

Collaborated with an international team to create co-living solutions for dense urban areas.

Focused on Japanese minimalism, multifunctional furniture, and sustainable material reuse.

UrbanScape Interiors, London, UK — Short-term Project Consultant (2023) (Imaginary but realistic)

Designed interior concepts for boutique retail stores and pop-up installations.

Applied VR modeling for client walkthroughs.

Mediterranean Design Lab, Naples, Italy — Research Assistant (2022) (Imaginary but realistic)

Investigated sustainable material alternatives for coastal urban housing projects.

Developed parametric models to optimize daylight exposure and energy efficiency.

Key Projects & Highlights

Delivered 50+ large-scale projects across Europe, North Africa, Middle East, and Asia.

Residential: Luxury villas, multi-generational family homes, eco-friendly apartments.

Commercial: Boutique hotels, coworking spaces, retail stores, office interiors.

Cultural: Museums, art galleries, urban heritage restorations.

Awards & Recognition:

Best Innovative Interior Design Concept, International Young Architects Forum, 2023 (imaginary)

Honorable Mention, Sustainable Urban Living Competition, Milan, 2022 (imaginary)

Skills & Tools: AutoCAD, Revit, SketchUp, Rhino + Grasshopper, V-Ray, Adobe Suite, BIM coordination.

Languages: English (Fluent), Spanish (Fluent), Italian (Intermediate), French (Conversational).

Currently designing a multi-generational family home in Barcelona, integrating smart systems, sustainable materials, and energy-efficient design.

If you want, I can take this expanded CV and generate a perfectly formatted YAML string that preserves all hierarchy and indentation so it’s ready for your system or a YAML resume generator.
"""

# ================= HELPERS =================

def generate_prompt(user_input: str) -> str:
    with open(PROMPT_TEMPLATE_FILE, "r") as f:
        template = f.read()
    return template.replace("{prompt}", user_input)

def call_ollama(prompt: str) -> str:
    print(f"Connecting to Ollama at {OLLAMA_HOST}...")
    
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    
    response.raise_for_status()
    return response.json()["response"]

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

def save_yaml(yaml_text: str):
    with open(OUTPUT_YAML, "w") as f:
        f.write(yaml_text)
    print(f"YAML saved to {OUTPUT_YAML}")
    

def run_rendercv():
    print("Running RenderCV...")
    
    cmd = [sys.executable, "-m", "rendercv", "render", OUTPUT_YAML]
    subprocess.run(cmd, check=True)
    
    print("\n--------------------------------")
    print("CV generated successfully!")
    print(f"Check folder: {RENDER_DIR}")
    print("--------------------------------")


# ================= MAIN PIPELINE =================

def main():
    try:
        print("Generating prompt...")
        prompt = generate_prompt(USER_INPUT)

        print("Calling Ollama...")
        ollama_output = call_ollama(prompt)

        print("\n--- RAW MODEL OUTPUT ---")
        print(ollama_output)

        print("\n--- EXTRACTED JSON ---")
        json_output = extract_json(ollama_output)
        print(json_output)

        print("\nConverting JSON → YAML...")
        yaml_text = json_to_yaml(json_output)

        print("\n--- GENERATED YAML ---")
        print(yaml_text)

        save_yaml(yaml_text)

        run_rendercv()

    except json.JSONDecodeError:
        print("\nERROR: Model did not return valid JSON.")
        print("You must enforce JSON-only in your prompt.")
    except subprocess.CalledProcessError:
        print("\nERROR: RenderCV failed.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
