course_builder/
  __init__.py
  __main__.py           # entrypoint: python -m course_builder
  models.py             # dataclasses: WeekPlan, CoursePlan
  io_prompts.py         # all user prompts & validation
  planner.py            # builds CoursePlan from inputs
  preview.py            # tree + calendar breakdown
  apply_local.py        # creates local directories/files
  google_integrations.py    # Drive/Calendar stubs (drop-in later)
  utils.py              # helpers: date/strings/tree rendering
