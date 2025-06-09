import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from server import server  # ton app FastAPI
from models.account import Account  # importe tes modèles ici

# Crée un moteur SQLite mémoire compatible multi-thread
test_engine = create_engine(
    "sqlite:///file::memory:?cache=shared",
    connect_args={"check_same_thread": False}
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    # override FastAPI dependency
    def get_session_override():
        yield session

    server.app.dependency_overrides = {}
    server.app.dependency_overrides[server.get_session] = get_session_override

    with TestClient(server.app) as c:
        yield c
