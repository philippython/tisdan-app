import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


def _to_uuid(item_id: Any) -> Any:
    """Convert string to UUID if needed — SQLite stores UUIDs as strings
    but SQLAlchemy's UUID type expects a uuid.UUID object for lookups."""
    if isinstance(item_id, str):
        try:
            return uuid.UUID(item_id)
        except ValueError:
            return item_id
    return item_id


def get_all_items(session: Session, model: Type[ModelType]) -> List[ModelType]:
    statement = select(model)
    return session.exec(statement).all()


def get_item_by_id(session: Session, model: Type[ModelType], item_id: Any) -> Optional[ModelType]:
    return session.get(model, _to_uuid(item_id))


def create_item(session: Session, model: Type[ModelType], data: Dict[str, Any]) -> ModelType:
    item = model(**data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_item(session: Session, model: Type[ModelType], item_id: Any, data: Dict[str, Any]) -> Optional[ModelType]:
    item = session.get(model, _to_uuid(item_id))
    if item is None:
        return None
    for key, value in data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, model: Type[ModelType], item_id: Any) -> bool:
    item = session.get(model, _to_uuid(item_id))
    if item is None:
        return False
    session.delete(item)
    session.commit()
    return True