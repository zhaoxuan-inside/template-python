from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateExampleCommand:
    name: str
    description: Optional[str] = None

@dataclass
class UpdateExampleCommand:
    id: int
    name: str
    description: Optional[str] = None

@dataclass
class DeleteExampleCommand:
    id: int
