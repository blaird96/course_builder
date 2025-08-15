# services/google/calendar_service.py
from course_builder.models import CoursePlan
from .common import build_calendar, all_day_exclusive_range

class CalendarService:
    def run(self, plan: CoursePlan, calendar_id: str = "primary") -> None:
        cal = build_calendar()
        if cal is None:
            print("[Calendar] Skipping Calendar integration - no valid credentials available.")
            return
            
        created = 0

        for w in plan.weeks:
            if not (w.start and w.end):
                continue  # skip undated weeks
            start_date, end_excl = all_day_exclusive_range(w.start, w.end)

            body = {
                "summary": f"{plan.course_name}: Week {w.index} — {w.title}",
                "description": f"{plan.course_name} — {w.title}",
                "start": {"date": start_date},
                "end": {"date": end_excl},  # exclusive
            }
            cal.events().insert(calendarId=calendar_id, body=body).execute()
            created += 1

        print(f"[Calendar] Created {created} all-day events on '{calendar_id}'.")
