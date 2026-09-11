import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


class ExperienceStore:
    """Small JSON-backed memory store for experiment experiences."""

    def __init__(self, path: str | Path = "aurora_memory.json") -> None:
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add(self, experience: dict[str, Any]) -> None:
        experiences = self.load()
        experiences.append(experience)
        self.path.write_text(
            json.dumps(experiences, indent=2), encoding="utf-8"
        )

    def count(self) -> int:
        return len(self.load())
