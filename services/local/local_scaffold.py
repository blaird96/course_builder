from .apply_local import apply_local
from course_builder.models import CoursePlan

class LocalScaffold:
    def run(self, plan: CoursePlan) -> None:
        apply_local(plan)
