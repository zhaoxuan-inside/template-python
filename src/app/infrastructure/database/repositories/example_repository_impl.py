from typing import Optional, Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.example.entities.example import Example
from app.domain.example.repositories.example_repository import ExampleRepository
from app.infrastructure.database.models.example import ExampleModel


class ExampleRepositoryImpl(ExampleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> Optional[Example]:
        stmt = select(ExampleModel).where(ExampleModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self) -> Sequence[Example]:
        stmt = select(ExampleModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_name(self, name: str) -> Optional[Example]:
        stmt = select(ExampleModel).where(ExampleModel.name == name)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, example: Example) -> Example:
        model = ExampleModel(name=example.name, description=example.description)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, example: Example) -> Example:
        stmt = (
            update(ExampleModel)
            .where(ExampleModel.id == example.id)
            .values(name=example.name, description=example.description)
        )
        await self._session.execute(stmt)
        await self._session.flush()

        stmt = select(ExampleModel).where(ExampleModel.id == example.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        return self._to_entity(model)

    async def delete(self, id: int) -> None:
        stmt = delete(ExampleModel).where(ExampleModel.id == id)
        await self._session.execute(stmt)

    @staticmethod
    def _to_entity(model: ExampleModel) -> Example:
        return Example(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
