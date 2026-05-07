import sys
import subprocess

from app import RENDER_DIR

def run_rendercv(yml: str):
    print("Running RenderCV...")
    
    cmd = [sys.executable, "-m", "rendercv", "render", yml]
    subprocess.run(cmd, check=True)
    
   
