from .cli.parser import parse_args
from .cli.controller import CourseBuilderController

# services live at top-level "services" package
from services.local.local_scaffold import LocalScaffold
from services.google.drive_service import DriveService
from services.google.calendar_service import CalendarService

def main():
    args = parse_args()

    controller = CourseBuilderController(
        local_action=LocalScaffold(),
        drive_action=DriveService(),
        calendar_action=CalendarService()
    )

    plan, interactive = controller.build_plan(args)
    controller.execute(
        plan,
        interactive=interactive,
        drive_flag=getattr(args, "drive", False),
        cal_flag=getattr(args, "calendar", False)
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
