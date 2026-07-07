from dataclasses import dataclass
from typing import Optional

from app.domain.shared.entity import Entity


@dataclass
class Example(Entity):
    id: int
    name: str
    description: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.name:
            raise ValueError("Name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Name cannot exceed 255 characters")
