from sqlmodel import Session, create_engine, select
from app.models import *
from app.core.config import settings

_connect_args = (
    {"check_same_thread": False}
    if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite")
    else {}
)
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    connect_args=_connect_args,
    pool_pre_ping=True,
)

if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    from sqlalchemy import event

    @event.listens_for(engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()



def init_db(session: Session) -> None:
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
