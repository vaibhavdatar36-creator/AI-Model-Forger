import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import tempfile
from app.core.path_resolver import resolve_dataset_path

def test_resolve_dataset_path_file():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(b"a,b\n1,2")
        temp_path = Path(f.name)
    try:
        resolved = resolve_dataset_path(temp_path)
        assert resolved == temp_path
    finally:
        if temp_path.exists():
            temp_path.unlink()

def test_resolve_dataset_path_dir_with_csv():
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        csv_path = dir_path / "subfolder" / "data.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_path.write_text("col1,col2\n1,2")

        # Resolves automatically
        resolved = resolve_dataset_path(dir_path)
        assert resolved == csv_path

        # Resolves with explicit TABULAR modality
        resolved_tab = resolve_dataset_path(dir_path, modality="TABULAR")
        assert resolved_tab == csv_path

def test_resolve_dataset_path_image_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        img_path = dir_path / "cats" / "cat1.jpg"
        img_path.parent.mkdir(parents=True, exist_ok=True)
        img_path.write_bytes(b"dummy image data")

        # Modality IMAGE preserves directory
        resolved_img = resolve_dataset_path(dir_path, modality="IMAGE")
        assert resolved_img == dir_path

        # Auto-detects image directory if no tabular files
        resolved_auto = resolve_dataset_path(dir_path)
        assert resolved_auto == dir_path
