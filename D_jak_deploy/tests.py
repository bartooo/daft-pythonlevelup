from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"msg": f"Hello {name}"}


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"
    # 3rd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "3"


def test_post_method():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}


def test_get_method():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_delete_method():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


def test_options_method():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


def test_put_method():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}