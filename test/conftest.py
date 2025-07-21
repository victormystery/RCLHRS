import pytest
from fastapi.testclient import TestClient
from main import app
from model import User, Role, Employee, BankRequests, DBSChecks, HomeOfficeRequests
from unittest.mock import MagicMock

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db(mocker):
    db = MagicMock()
    return db

@pytest.fixture
def mock_user_admin():
    user = MagicMock(spec=User)
    user.username = "adminuser"
    role = MagicMock(spec=Role)
    role.role_name = "admin"
    role.is_admin = True
    role.is_hr = False
    user.role = role
    return user

@pytest.fixture
def mock_user_hr():
    user = MagicMock(spec=User)
    user.username = "hruser"
    role = MagicMock(spec=Role)
    role.role_name = "hr"
    role.is_hr = True
    role.is_admin = False
    user.role = role
    return user

@pytest.fixture
def mock_user_regular():
    user = MagicMock(spec=User)
    user.username = "regularuser"
    role = MagicMock(spec=Role)
    role.role_name = "user"
    role.is_hr = False
    role.is_admin = False
    user.role = role
    return user