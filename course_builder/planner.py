from datetime import timedelta
from typing import List
from .models import CoursePlan, WeekPlan
from .io_prompts import Prompt

def build_course_plan() -> CoursePlan:
    prompt = Prompt()

    print("\n=== Course Directory Builder ===\n")
    root = prompt.path("Select or create your course root directory (e.g., ~/home/umgc/cmsc320):")
    course_name = input("Course name/label (e.g., 'CMSC 320'): ").strip() or root.name

    n_weeks = prompt.integer("How many weeks in the course?")
    print("\nEnter titles for each week (e.g., 'Entities and Attributes').")
    weeks: List[WeekPlan] = []
    for i in range(1, n_weeks + 1):
        title = input(f"Title for Week {i}: ").strip() or f"Week_{i}"
        weeks.append(WeekPlan(index=i, title=title))

    if prompt.yes_no("\nDo you want to specify dates? (per-week or auto-fill from a start date)"):
        mode_auto = prompt.yes_no("Auto-fill weekly ranges from a single course start date?")
        if mode_auto:
            start = prompt.date("Course start date (Monday recommended)")
            if start:
                for w in weeks:
                    w.start = start + timedelta(days=(w.index - 1) * 7)
                    w.end   = w.start + timedelta(days=6)
        else:
            print("Enter start/end dates per week (blank to skip).")
            for w in weeks:
                w.start = prompt.date(f"Week {w.index} start")
                w.end   = prompt.date(f"Week {w.index} end")

    return CoursePlan(root=root, course_name=course_name, weeks=weeks)
