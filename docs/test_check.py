import os
import sys
from pathlib import Path
from pypdf import PdfReader

# Verify directories
base_dir = Path(r"C:\Users\Vaibhav\.gemini\antigravity\scratch\ai-model-forge")
docs_dir = base_dir / "docs"
docs_dir.mkdir(parents=True, exist_ok=True)
logo_path = docs_dir / "extracted_template" / "image1.png"

print("Checking logo exists:", logo_path.exists())
