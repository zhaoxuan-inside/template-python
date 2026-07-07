from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Example:
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Name cannot exceed 255 characters")
