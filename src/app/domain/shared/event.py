from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainEvent(ABC):
    event_id: str
    occurred_at: datetime
    aggregate_id: int

    def __post_init__(self) -> None:
        if self.occurred_at is None:
            self.occurred_at = datetime.utcnow()
