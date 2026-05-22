from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


def get_all_items(session: Session, model: Type[ModelType]) -> List[ModelType]:
    statement = select(model)
    return session.exec(statement).all()


def get_item_by_id(session: Session, model: Type[ModelType], item_id: Any) -> Optional[ModelType]:
    return session.get(model, item_id)


def create_item(session: Session, model: Type[ModelType], data: Dict[str, Any]) -> ModelType:
    item = model(**data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_item(session: Session, model: Type[ModelType], item_id: Any, data: Dict[str, Any]) -> Optional[ModelType]:
    item = session.get(model, item_id)
    if item is None:
        return None
    for key, value in data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, model: Type[ModelType], item_id: Any) -> bool:
    item = session.get(model, item_id)
    if item is None:
        return False
    session.delete(item)
    session.commit()
    return True
