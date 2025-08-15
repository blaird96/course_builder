from .models import CoursePlan

def push_to_google_drive(course: CoursePlan) -> None:
    print("[INFO] (stub) Would create mirrored folders in Google Drive.")

def push_to_google_calendar(course: CoursePlan) -> None:
    print("[INFO] (stub) Would create Google Calendar events for dated weeks.")
