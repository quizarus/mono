from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, RelationshipDirection, lazyload

from app.database import get_db
from app.models import BaseModel


class BaseEntityManager:

    model: BaseModel

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.obj = None

    async def get(self, pk: int, relations: list[str] | None = None, *args, **kwargs) -> BaseModel:
        stmt = select(self.model).where(self.model.id == pk)
        if relations:
            relation_fields = [getattr(self.model, relation) for relation in relations]
            stmt = stmt.options(*[joinedload(field) for field in relation_fields])
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_all(self, load_relations: bool = True, *args, **kwargs) -> list[BaseModel]:

        stmt = select(self.model)
        if not load_relations:
            stmt = stmt.options(lazyload('*'))
        result = await self.db.execute(stmt)
        objects = result.unique().scalars().all()
        return objects

    async def commit(self):
        await self.db.commit()
        await self.db.refresh(self.obj)

    async def create(self, commit: bool = True, *args, **kwargs) -> BaseModel:
        obj = self.model()
        self.obj = obj
        obj, attrs = await self.__update_m2m_relations(obj, kwargs)

        for k, v in attrs.items():
            setattr(obj, k, v)

        self.db.add(obj)

        if commit:
            await self.commit()

        return obj

    async def update(self, pk: int, commit: bool = True, *args, **kwargs) -> BaseModel:
        obj = await self.get(pk)
        obj, attrs = await self.__update_m2m_relations(obj, kwargs)

        for k, v in attrs.items():
            setattr(obj, k, v)
        self.db.add(obj)

        if commit:
            await self.db.commit()
            await self.db.refresh(obj)

        return obj

    async def delete(self, pk: int, commit: bool = True, *args, **kwargs):
        obj = await self.get(pk)

        if commit:
            await self.db.delete(obj)
            await self.db.commit()

    async def __update_m2m_relations(self, obj: BaseModel, attrs: dict) -> tuple[BaseModel, dict]:

        async def update(field: str, idents: list[int]):
            model = getattr(self.model, field).comparator.mapper.class_
            attribute = getattr(model, 'id')
            stmt = select(model).where(attribute.in_(idents))
            result = await self.db.execute(stmt)
            related_objects = result.scalars().all()
            if diff := set(idents) - set([getattr(rel_obj, 'id') for rel_obj in related_objects]):
                raise HTTPException(status_code=404, detail=f"{model.__name__} does not exists: {[_ for _ in diff]}")
            setattr(obj, field, related_objects)

        for attr in attrs.copy():
            model_attr = getattr(obj.__class__, attr, None)
            if not (model_attr and hasattr(model_attr.prop, 'direction') and model_attr.prop.direction == RelationshipDirection.MANYTOMANY):
                continue
            idents = attrs.pop(attr)
            await update(attr, idents)

        return obj, attrs

