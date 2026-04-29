from __future__ import annotations

import re
from pathlib import Path
from typing import Dict
from zipfile import ZipFile


def _extract_docx_text(path: Path) -> str:
    with ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    text = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    text = re.sub(r"</w:p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def read_text(path: str) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8")
    if suffix == ".docx":
        return _extract_docx_text(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")


def load_inputs(resume_path: str, jd_path: str) -> Dict[str, str]:
    return {
        "resume_text": read_text(resume_path),
        "jd_text": read_text(jd_path),
    }
