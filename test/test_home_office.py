import pytest
from fastapi import HTTPException
from model import HomeOfficeRequests
from schemas import HomeOfficeRequestOut

def test_get_home_office_requests(client, mocker, mock_user_admin):
    mocker.patch("auth.dependencies.get_current_user", return_value=mock_user_admin)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.query().all.return_value = [
        MagicMock(id=1, request_type="Visa", status="Pending", employee_id=1)
    ]
    response = client.get("/home_office_requests/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["request_type"] == "Visa"

def test_get_home_office_request(client, mocker, mock_user_admin):
    mocker.patch("auth.dependencies.get_current_user", return_value=mock_user_admin)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.query().filter().first.return_value = MagicMock(id=1, request_type="Visa", status="Pending", employee_id=1)
    response = client.get("/home_office_requests/1")
    assert response.status_code == 200
    assert response.json()["request_type"] == "Visa"

def test_get_home_office_request_not_found(client, mocker, mock_user_admin):
    mocker.patch("auth.dependencies.get_current_user", return_value=mock_user_admin)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.query().filter().first.return_value = None
    response = client.get("/home_office_requests/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Home Office request not found"

def test_create_home_office_request(client, mocker, mock_user_hr):
    mocker.patch("auth.dependencies.require_hr", return_value=mock_user_hr)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, "id", 1)
    response = client.post("/home_office_requests/", json={"request_type": "Visa", "status": "Pending", "employee_id": 1})
    assert response.status_code == 200
    assert response.json()["request_type"] == "Visa"

def test_create_home_office_request_unauthorized(client, mocker, mock_user_regular):
    mocker.patch("auth.dependencies.require_hr", side_effect=HTTPException(status_code=403, detail="HR access required"))
    response = client.post("/home_office_requests/", json={"request_type": "Visa", "status": "Pending", "employee_id": 1})
    assert response.status_code == 403
    assert response.json()["detail"] == "HR access required"

def test_update_home_office_request(client, mocker, mock_user_hr):
    mocker.patch("auth.dependencies.require_hr", return_value=mock_user_hr)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.query().filter().first.return_value = MagicMock(id=1, request_type="Visa", status="Pending", employee_id=1)
    response = client.put("/home_office_requests/1", json={"status": "Approved"})
    assert response.status_code == 200
    assert response.json()["status"] == "Approved"

def test_delete_home_office_request(client, mocker, mock_user_admin):
    mocker.patch("auth.dependencies.require_admin", return_value=mock_user_admin)
    mock_db = mocker.patch("database.get_db").return_value
    mock_db.query().filter().first.return_value = MagicMock(id=1)
    response = client.delete("/home_office_requests/1")
    assert response.status_code == 204

def test_delete_home_office_request_unauthorized(client, mocker, mock_user_regular):
    mocker.patch("auth.dependencies.require_admin", side_effect=HTTPException(status_code=403, detail="Admin access required"))
    response = client.delete("/home_office_requests/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"