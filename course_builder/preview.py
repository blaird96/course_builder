from .models import CoursePlan
from .utils import ascii_tree, format_week_folder, format_dates

def preview_plan(plan: CoursePlan) -> None:
    subdirs = [format_week_folder(w.index, w.title) for w in plan.weeks]
    print("\n--- Directory preview ---")
    print(ascii_tree(plan.root, subdirs))

    print("\n--- Calendar breakdown ---")
    for w in plan.weeks:
        print(f"Week {w.index}: {w.title}   |   {format_dates(w.start, w.end)}")
