# services/google/drive_service.py
from course_builder.models import CoursePlan
from course_builder.utils import format_week_folder
from .common import build_drive, ensure_drive_folder

class DriveService:
    def run(self, plan: CoursePlan) -> None:
        drive = build_drive()
        if drive is None:
            print("[Drive] Skipping Drive integration - no valid credentials available.")
            return

        # Ensure top-level course folder
        course_id = ensure_drive_folder(drive, plan.course_name)

        # Ensure each week subfolder
        for w in plan.weeks:
            week_name = format_week_folder(w.index, w.title)
            ensure_drive_folder(drive, week_name, parent_id=course_id)

        print(f"[Drive] Ensured folder '{plan.course_name}' with {len(plan.weeks)} week subfolders.")
