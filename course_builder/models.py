from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional

@dataclass
class WeekPlan:
    index: int
    title: str
    start: Optional[date] = None
    end: Optional[date] = None

@dataclass
class CoursePlan:
    root: Path
    course_name: str
    weeks: List[WeekPlan]