# course_builder/cli/controller.py
from ..models import CoursePlan
from ..io_prompts import Prompt
from ..preview import preview_plan
from .build_from_args import build_from_args

class CourseBuilderController:
    def __init__(self, local_action, drive_action=None, calendar_action=None):
        self.local_action = local_action
        self.drive_action = drive_action
        self.calendar_action = calendar_action  # <-- make sure this exists

    def build_plan(self, args):
        plan = build_from_args(args)
        if plan:
            return plan, False  # headless mode
        from ..planner import build_course_plan
        return build_course_plan(), True  # interactive mode

    def _confirm(self) -> bool:
        return Prompt().yes_no("\nDoes this look correct?", default=True)

    def execute(self, plan: CoursePlan, *, interactive: bool, drive_flag: bool, cal_flag: bool):
        preview_plan(plan)

        if interactive:
            if not self._confirm():
                print("Aborted by user. No changes made.")
                return
            self.local_action.run(plan)
            prompt = Prompt()
            if self.drive_action and prompt.yes_no("\nAlso mirror to Google Drive now?"):
                self.drive_action.run(plan)
            if self.calendar_action and prompt.yes_no("Create Google Calendar entries for dated weeks?"):
                self.calendar_action.run(plan)
        else:
            self.local_action.run(plan)
            if self.drive_action and drive_flag:
                self.drive_action.run(plan)
            if self.calendar_action and cal_flag:
                self.calendar_action.run(plan)

        print("\nAll set.")
