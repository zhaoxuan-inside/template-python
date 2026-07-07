from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.example.commands.example_commands import (
    CreateExampleCommand,
    DeleteExampleCommand,
    UpdateExampleCommand,
)
from app.application.example.dtos.example_dtos import (
    ExampleCreateDTO,
    ExampleResponseDTO,
    ExampleUpdateDTO,
)
from app.application.example.queries.example_queries import (
    GetAllExamplesQuery,
    GetExampleQuery,
)
from app.application.example.use_cases.example_use_cases import ExampleUseCases
from app.domain.example.exceptions.example_exceptions import (
    ExampleAlreadyExistsError,
    ExampleNotFoundError,
)
from app.domain.example.repositories.example_repository import ExampleRepository
from app.domain.example.services.example_service import ExampleService
from app.infrastructure.database.core import get_db
from app.infrastructure.database.repositories.example_repository_impl import (
    ExampleRepositoryImpl,
)

router = APIRouter(prefix="/examples", tags=["examples"])


async def get_example_use_cases(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> tuple[ExampleUseCases, AsyncSession]:
    repository: ExampleRepository = ExampleRepositoryImpl(db)
    service = ExampleService(repository)
    return ExampleUseCases(service), db


@router.get("", response_model=Sequence[ExampleResponseDTO])
async def get_all_examples(use_cases: Annotated[tuple, Depends(get_example_use_cases)]):
    query = GetAllExamplesQuery()
    return await use_cases[0].handle_get_all_examples(query)


@router.get("/{example_id}", response_model=ExampleResponseDTO)
async def get_example(
    example_id: int,
    use_cases: Annotated[tuple, Depends(get_example_use_cases)],
):
    try:
        query = GetExampleQuery(id=example_id)
        return await use_cases[0].handle_get_example(query)
    except ExampleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("", response_model=ExampleResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_example(
    dto: ExampleCreateDTO,
    use_cases: Annotated[tuple, Depends(get_example_use_cases)],
):
    try:
        command = CreateExampleCommand(name=dto.name, description=dto.description)
        result = await use_cases[0].handle_create_example(command)
        await use_cases[1].commit()
        return result
    except ExampleAlreadyExistsError as e:
        await use_cases[1].rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.put("/{example_id}", response_model=ExampleResponseDTO)
async def update_example(
    example_id: int,
    dto: ExampleUpdateDTO,
    use_cases: Annotated[tuple, Depends(get_example_use_cases)],
):
    try:
        command = UpdateExampleCommand(id=example_id, name=dto.name, description=dto.description)
        result = await use_cases[0].handle_update_example(command)
        await use_cases[1].commit()
        return result
    except ExampleNotFoundError as e:
        await use_cases[1].rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    example_id: int,
    use_cases: Annotated[tuple, Depends(get_example_use_cases)],
):
    try:
        command = DeleteExampleCommand(id=example_id)
        await use_cases[0].handle_delete_example(command)
        await use_cases[1].commit()
    except ExampleNotFoundError as e:
        await use_cases[1].rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
