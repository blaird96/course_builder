# api/main.py
from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- domain imports (your code) ---
from course_builder.models import CoursePlan, WeekPlan
from course_builder.utils import format_week_folder, format_dates
from services.local.local_scaffold import LocalScaffold
from services.google.drive_service import DriveService
from services.google.calendar_service import CalendarService


# =========================
# Settings / configuration
# =========================
@dataclass
class Settings:
    title: str = "Course Builder API"
    version: str = "0.1.0"
    cors_origins: List[str] = None

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]


# ================
# API DTO schemas
# ================
class WeekIn(BaseModel):
    index: int
    title: str
    start: Optional[date] = None
    end: Optional[date] = None

class PlanIn(BaseModel):
    root: str
    course_name: str
    weeks: List[WeekIn] = Field(default_factory=list)

class PreviewOut(BaseModel):
    tree: List[str]
    calendar: List[str]


# ==========================
# Controller / use-case layer
# ==========================
class PlanController:
    """Thin application service that coordinates your domain/services."""

    def __init__(
        self,
        local: LocalScaffold,
        drive: Optional[DriveService] = None,
        calendar: Optional[CalendarService] = None,
    ):
        self.local = local
        # Avoid shadowing endpoint methods named `drive` and `calendar`
        self.drive_service = drive
        self.calendar_service = calendar

    # ---- helpers ----
    @staticmethod
    def _to_course_plan(p: PlanIn) -> CoursePlan:
        root = Path(p.root).expanduser().resolve()
        weeks = [WeekPlan(w.index, w.title, w.start, w.end) for w in p.weeks]
        return CoursePlan(root=root, course_name=p.course_name, weeks=weeks)

    @staticmethod
    def _dir_tree_lines(plan: CoursePlan) -> List[str]:
        return [str(plan.root)] + [f"└── {format_week_folder(w.index, w.title)}" for w in plan.weeks]

    @staticmethod
    def _calendar_lines(plan: CoursePlan) -> List[str]:
        return [f"Week {w.index}: {w.title} | {format_dates(w.start, w.end)}" for w in plan.weeks]

    # ---- endpoints (called by router) ----
    def autofill(self, root: str, course_name: str, weeks: int, start: Optional[date] = None) -> PlanIn:
        items: List[WeekIn] = []
        for i in range(1, weeks + 1):
            s = e = None
            if start:
                s = start + timedelta(days=(i - 1) * 7)
                e = s + timedelta(days=6)
            items.append(WeekIn(index=i, title=f"Week_{i}", start=s, end=e))
        return PlanIn(root=root, course_name=course_name, weeks=items)

    def preview(self, plan_in: PlanIn) -> PreviewOut:
        cp = self._to_course_plan(plan_in)
        return PreviewOut(tree=self._dir_tree_lines(cp), calendar=self._calendar_lines(cp))

    def scaffold(self, plan_in: PlanIn) -> dict:
        self.local.run(self._to_course_plan(plan_in))
        return {"ok": True}

    def drive(self, plan_in: PlanIn) -> dict:
        if not self.drive_service:
            return {"ok": False, "error": "Drive service not configured"}
        self.drive_service.run(self._to_course_plan(plan_in))
        return {"ok": True}

    def calendar(self, plan_in: PlanIn) -> dict:
        if not self.calendar_service:
            return {"ok": False, "error": "Calendar service not configured"}
        self.calendar_service.run(self._to_course_plan(plan_in))
        return {"ok": True}


# ==========================
# Router / app wiring layer
# ==========================
def build_router(controller: PlanController) -> APIRouter:
    router = APIRouter()

    @router.post("/plan/autofill", response_model=PlanIn)
    def autofill(root: str, course_name: str, weeks: int, start: Optional[date] = None):
        return controller.autofill(root, course_name, weeks, start)

    @router.post("/plan/preview", response_model=PreviewOut)
    def preview(plan: PlanIn):
        return controller.preview(plan)

    @router.post("/scaffold")
    def scaffold(plan: PlanIn):
        return controller.scaffold(plan)

    @router.post("/drive")
    def drive(plan: PlanIn):
        return controller.drive(plan)

    @router.post("/calendar")
    def calendar(plan: PlanIn):
        return controller.calendar(plan)

    return router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    # Instantiate services (DI)
    controller = PlanController(
        local=LocalScaffold(),
        drive=DriveService(),
        calendar=CalendarService(),
    )

    app = FastAPI(title=settings.title, version=settings.version)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(build_router(controller))

    return app


# Uvicorn entrypoint: `uvicorn api.main:app --reload`
app = create_app()
