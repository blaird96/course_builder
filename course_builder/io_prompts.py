from pathlib import Path
from datetime import date
from typing import Optional, Callable

class Prompt:
    def __init__(self, reader: Callable[[str], str] = input, writer: Callable[[str], None] = print):
        self.reader = reader
        self.writer = writer

    def _ask(self, message: str) -> str:
        return self.reader(message.rstrip() + " ").strip()

    def path(self, message: str) -> Path:
        while True:
            raw = self._ask(message)
            p = Path(raw).expanduser().resolve()
            if p.exists() and p.is_dir():
                return p
            if not p.exists():
                yn = self._ask("Path does not exist. Create it? (y/n):").lower()
                if yn in ("y", "yes"):
                    try:
                        p.mkdir(parents=True, exist_ok=True)
                        return p
                    except Exception as e:
                        self.writer(f"Error creating directory: {e}")
                continue
            self.writer("That path exists but is not a directory.")

    def integer(self, message: str, min_value: int = 1, max_value: Optional[int] = None) -> int:
        while True:
            raw = self._ask(message)
            try:
                n = int(raw)
                if n < min_value:
                    self.writer(f"Enter a number ≥ {min_value}."); continue
                if max_value is not None and n > max_value:
                    self.writer(f"Enter a number ≤ {max_value}."); continue
                return n
            except ValueError:
                self.writer("Please enter a valid integer.")

    def yes_no(self, message: str, default: bool = False) -> bool:
        default_str = "Y/n" if default else "y/N"
        while True:
            raw = self._ask(f"{message} [{default_str}]:").lower()
            if raw == "":
                return default
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            self.writer("Please answer y or n.")

    def date(self, message: str) -> Optional[date]:
        while True:
            raw = self._ask(f"{message} (YYYY-MM-DD or leave empty):")
            if not raw:
                return None
            try:
                y, m, d = map(int, raw.split("-"))
                return date(y, m, d)
            except Exception:
                self.writer("Invalid date format. Please use YYYY-MM-DD.")
