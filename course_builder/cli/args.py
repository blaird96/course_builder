from enum import Enum

class Args(Enum):
    ROOT = ("--root", dict(type=str, help="Root directory for the course builder."))
    NAME = ("--name", dict(type=str, help="Course name/label"))
    WEEKS = ("--weeks", dict(type=int, help="Number of weeks in the course."))
    START = ("--start", dict(type=str, help="Start date of the course in YYYY-MM-DD format."))
    DRIVE = ("--drive", dict(action="store_true", help="Mirror to Google Drive."))
    CALENDAR = ("--calendar", dict(action="store_true", help="Create Google Calendar events."))

    @property
    def flag(self) -> str:
        return self.value[0]
    
    @property
    def kwargs(self) -> dict:
        return self.value[1]
