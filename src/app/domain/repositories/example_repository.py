from abc import ABC, abstractmethod
from typing import Optional, Sequence

from app.domain.entities.example import Example


class ExampleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Example]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Example]:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[Example]:
        pass

    @abstractmethod
    async def create(self, example: Example) -> Example:
        pass

    @abstractmethod
    async def update(self, example: Example) -> Example:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
