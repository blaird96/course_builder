from course_builder.models import CoursePlan
from course_builder.utils import format_week_folder, format_dates


def apply_local(plan: CoursePlan) -> None:
    print("\nCreating directories locally...")
    created = 0
    for w in plan.weeks:
        folder = plan.root / format_week_folder(w.index, w.title)
        try:
            folder.mkdir(parents=True, exist_ok=True)
            readme = folder / "README.md"
            if not readme.exists():
                readme.write_text(
                    f"# {plan.course_name} — Week {w.index}: {w.title}\n\n"
                    f"- Dates: {format_dates(w.start, w.end)}\n"
                )
            created += 1
        except Exception as e:
            print(f"[ERROR] Could not create {folder}: {e}")
    print(f"Done. {created} week folders ensured.")
