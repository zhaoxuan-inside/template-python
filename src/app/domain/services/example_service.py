from typing import Optional, Sequence

from app.domain.entities.example import Example
from app.domain.exceptions.example_exceptions import ExampleAlreadyExistsError, ExampleNotFoundError
from app.domain.repositories.example_repository import ExampleRepository


class ExampleService:
    def __init__(self, repository: ExampleRepository) -> None:
        self._repository = repository

    async def get_example(self, example_id: int) -> Example:
        example = await self._repository.get_by_id(example_id)
        if not example:
            raise ExampleNotFoundError(example_id)
        return example

    async def get_all_examples(self) -> Sequence[Example]:
        return await self._repository.get_all()

    async def create_example(self, name: str, description: Optional[str] = None) -> Example:
        existing_example = await self._repository.get_by_name(name)
        if existing_example:
            raise ExampleAlreadyExistsError(name)

        example = Example(id=0, name=name, description=description)
        return await self._repository.create(example)

    async def update_example(self, example_id: int, name: str, description: Optional[str] = None) -> Example:
        await self.get_example(example_id)

        example = Example(id=example_id, name=name, description=description)
        return await self._repository.update(example)

    async def delete_example(self, example_id: int) -> None:
        await self.get_example(example_id)
        await self._repository.delete(example_id)
