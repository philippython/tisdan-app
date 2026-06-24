from sqlmodel import Session, create_engine, select
from app.models import *
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))



def init_db(session: Session) -> None:
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
