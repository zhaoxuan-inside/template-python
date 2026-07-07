from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Name cannot be empty")
        if len(self.value) > 255:
            raise ValueError("Name cannot exceed 255 characters")
