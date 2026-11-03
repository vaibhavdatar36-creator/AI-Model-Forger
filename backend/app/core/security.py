import os
import re
import hashlib
import zipfile
from pathlib import Path
from typing import List, Tuple
from app.core.logging import logger

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and invalid characters."""
    clean = os.path.basename(filename)
    clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    return clean

def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def is_safe_zip_path(target_dir: Path, member_path: str) -> bool:
    """Check if the zip entry path resolves safely inside target_dir (prevent Zip Slip)."""
    target_dir = target_dir.resolve()
    dest = (target_dir / member_path).resolve()
    return dest.is_relative_to(target_dir)

def safe_extract_zip(zip_path: Path, target_dir: Path) -> List[Path]:
    """Safely extract zip archive files, rejecting malicious path traversal entries."""
    target_dir.mkdir(parents=True, exist_ok=True)
    extracted_files = []
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for member in zf.infolist():
            # Skip entries with path traversal patterns or absolute paths
            if not is_safe_zip_path(target_dir, member.filename):
                logger.warning(f"Skipping suspicious zip member: {member.filename}")
                continue
            
            # Skip hidden metadata files like __MACOSX or .DS_Store
            if "__MACOSX" in member.filename or member.filename.startswith("."):
                continue
                
            extracted_path = target_dir / member.filename
            if member.is_dir():
                extracted_path.mkdir(parents=True, exist_ok=True)
            else:
                extracted_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as source, open(extracted_path, "wb") as target:
                    target.write(source.read())
                extracted_files.append(extracted_path)
                
    return extracted_files
