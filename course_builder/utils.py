# course_builder/utils.py
from pathlib import Path
from datetime import date
from typing import List, Optional

def safe_slug(s: str) -> str:
    return "_".join(s.strip().split())

def format_week_folder(i: int, title: str) -> str:
    return f"Week_{i}_{safe_slug(title)}"

def format_dates(s: Optional[date], e: Optional[date]) -> str:
    if s and e:  return f"{s.isoformat()} → {e.isoformat()}"
    if s and not e:  return f"{s.isoformat()} → (unspecified)"
    if not s and e:  return f"(unspecified) → {e.isoformat()}"
    return "(no dates specified)"

def ascii_tree(root: Path, subdirs: List[str]) -> str:
    lines = [str(root)]
    for i, s in enumerate(subdirs):
        tee = "└── " if i == len(subdirs) - 1 else "├── "
        lines.append(f"{tee}{s}")
    return "\n".join(lines)
