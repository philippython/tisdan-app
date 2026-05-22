from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlmodel import Session, SQLModel

from repositories.repository import (
    create_item,
    delete_item,
    get_all_items,
    get_item_by_id,
    update_item,
)

ModelType = TypeVar("ModelType", bound=SQLModel)


def list_resources(model: Type[ModelType], session: Session) -> List[ModelType]:
    return get_all_items(session, model)


def get_resource(model: Type[ModelType], resource_id: Any, session: Session) -> Optional[ModelType]:
    return get_item_by_id(session, model, resource_id)


def create_resource(payload: Any, model: Type[ModelType], session: Session) -> ModelType:
    data = payload.dict(exclude_none=True)
    return create_item(session, model, data)


def update_resource(payload: Any, model: Type[ModelType], resource_id: Any, session: Session) -> Optional[ModelType]:
    data = payload.dict(exclude_none=True)
    return update_item(session, model, resource_id, data)


def delete_resource(model: Type[ModelType], resource_id: Any, session: Session) -> bool:
    return delete_item(session, model, resource_id)
