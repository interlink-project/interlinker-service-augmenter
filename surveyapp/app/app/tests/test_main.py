import json

import pytest

from app import crud
from app.defaults import formio
# https://testdriven.io/blog/fastapi-crud/
# https://github.com/testdrivenio/fastapi-crud-async/blob/master/src/tests/test_notes.py
from app import database

async def get_collection_mock(payload):
    print("HACE ESTO")
    return True

def test_ping(test_app):
    response = test_app.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == True


def test_endpoints(test_app, monkeypatch):
    response = test_app.get(f"/assets/instantiate")
    assert response.status_code == 200

    id = "bb6bae15bbb9497c90e8a91cddc35654"
    send_payload = {
        "description": "sdfsdf",
        "title": "sdfsd"
    }
    response_payload = send_payload
    response_payload["_id"] = id

    async def mock(payload):
        return response_payload

    monkeypatch.setattr(database, "get_collection", get_collection_mock)

    monkeypatch.setattr(crud, "create", mock)
    monkeypatch.setattr(crud, "get", mock)

    response = test_app.post("/api/v1/assets", json=send_payload)
    print(response.json())
    assert response.status_code == 201
"""
def test_create_asset(test_app, monkeypatch):
    test_payload = formio

    response_payload = test_payload
    response_payload["_id"] = "EXAMPLEID"
    response_payload["name"] = "EXAMPLENAME"

    async def mock_create(payload):
        return response_payload

    monkeypatch.setattr(crud, "create", mock_create)
    response = test_app.post("/api/v1/surveys/", json=test_payload)

    assert response.status_code == 201
    assert response.json() == response_payload



def test_create_asset_invalid_json(test_app):
    response = test_app.post("/api/v1/assets/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422

    response = test_app.post("/api/v1/assets/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == 422


def test_read_asset(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something", "description": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/api/v1/assets/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_asset_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/api/v1/assets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"

    response = test_app.get("/api/v1/assets/0")
    assert response.status_code == 422


def test_read_all_assets(test_app, monkeypatch):
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/api/v1/assets/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_asset(test_app, monkeypatch):
    test_update_data = {"title": "someone", "description": "someone else", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/api/v1/assets/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_asset_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/api/v1/assets/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_asset(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/api/v1/assets/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_asset_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/api/v1/assets/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found"

    response = test_app.delete("/api/v1/assets/0/")
    assert response.status_code == 422
"""
