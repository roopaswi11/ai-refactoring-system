import zipfile
from pathlib import Path

def extract_zip(zip_path: str, extract_to: str):
    extract_path = Path(extract_to)
    extract_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path