from dataclasses import dataclass

from app.domain.shared.value_object import ValueObject


@dataclass(frozen=True)
class Name(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Name cannot be empty")
        if len(self.value) > 255:
            raise ValueError("Name cannot exceed 255 characters")
