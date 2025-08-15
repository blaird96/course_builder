from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from ..models import CoursePlan, WeekPlan

def build_from_args(args) -> Optional[CoursePlan]:
    """
    Returns a CoursePlan if sufficient args were provided (root + weeks).
    Otherwise returns None to signal 'fall back to interactive flow'.
    """
    if not (args.root and args.weeks):
        return None

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    course_name = args.name or root.name

    # Minimal week skeleton; titles can be edited later or left as Week_i
    weeks = [WeekPlan(i, f"Week_{i}") for i in range(1, args.weeks + 1)]

    if args.start:
        s = date.fromisoformat(args.start)
        for w in weeks:
            w.start = s + timedelta(days=(w.index - 1) * 7)
            w.end   = w.start + timedelta(days=6)

    return CoursePlan(root, course_name, weeks)
