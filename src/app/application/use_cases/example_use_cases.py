from typing import Sequence

from app.application.commands.example_commands import (
    CreateExampleCommand,
    DeleteExampleCommand,
    UpdateExampleCommand,
)
from app.application.dtos.example_dtos import ExampleResponseDTO
from app.application.queries.example_queries import (
    GetAllExamplesQuery,
    GetExampleQuery,
)
from app.domain.entities.example import Example
from app.domain.services.example_service import ExampleService


class ExampleUseCases:
    def __init__(self, service: ExampleService) -> None:
        self._service = service

    async def handle_get_example(self, query: GetExampleQuery) -> ExampleResponseDTO:
        example = await self._service.get_example(query.id)
        return self._to_response_dto(example)

    async def handle_get_all_examples(self, query: GetAllExamplesQuery) -> Sequence[ExampleResponseDTO]:
        examples = await self._service.get_all_examples()
        return [self._to_response_dto(e) for e in examples]

    async def handle_create_example(self, command: CreateExampleCommand) -> ExampleResponseDTO:
        example = await self._service.create_example(command.name, command.description)
        return self._to_response_dto(example)

    async def handle_update_example(self, command: UpdateExampleCommand) -> ExampleResponseDTO:
        example = await self._service.update_example(command.id, command.name, command.description)
        return self._to_response_dto(example)

    async def handle_delete_example(self, command: DeleteExampleCommand) -> None:
        await self._service.delete_example(command.id)

    @staticmethod
    def _to_response_dto(example: Example) -> ExampleResponseDTO:
        return ExampleResponseDTO(
            id=example.id,
            name=example.name,
            description=example.description,
            created_at=example.created_at,
            updated_at=example.updated_at,
        )
