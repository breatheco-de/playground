import os

from sqlmodel import (
    Session, SQLModel, create_engine
)

engine = create_engine(
    os.getenv("DB_URL", "sqlite:///./playground.sqlite")
)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    # Ensure all declared SQLModel tables exist before serving requests.
    SQLModel.metadata.create_all(engine)
