from dataclasses import dataclass

from app.domain.shared.event import DomainEvent


@dataclass
class ExampleCreatedEvent(DomainEvent):
    name: str
    description: str | None


@dataclass
class ExampleUpdatedEvent(DomainEvent):
    name: str
    description: str | None


@dataclass
class ExampleDeletedEvent(DomainEvent):
    pass
