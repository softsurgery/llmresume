import sys
import subprocess
from pathlib import Path


def run_rendercv(yaml_path: str, output_dir: str):
    """Run RenderCV to generate CV files from a YAML input."""
    print("Running RenderCV...")

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, "-m", "rendercv", "render", yaml_path, "--output-folder", output_dir]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path(yaml_path).parent))

    if result.returncode != 0:
        print(f"RenderCV stdout:\n{result.stdout}")
        print(f"RenderCV stderr:\n{result.stderr}")
        raise RuntimeError(f"RenderCV failed with exit code {result.returncode}: {result.stderr}")

    print(f"RenderCV output generated successfully")
