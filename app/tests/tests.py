from fastapi.testclient import TestClient
import pytest
from datetime import date, timedelta, datetime

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


def test_auth():
    response = client.get(
        "/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215"
    )
    assert response.status_code == 204
    response = client.get(
        "/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091"
    )
    assert response.status_code == 401


def test_register():
    response = client.post("/register/", json={"name": "Jan", "surname": "Nowak"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowak",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=8)).isoformat(),
    }

    response = client.post("/register/", json={"name": "Adam", "surname": "Kowalski"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "name": "Adam",
        "surname": "Kowalski",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=12)).isoformat(),
    }

    response = client.post(
        "/register/", json={"name": "Marek11", "surname": "Witkowski200"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "name": "Marek11",
        "surname": "Witkowski200",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=14)).isoformat(),
    }


def test_patient():
    response = client.get("/patient/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowak",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=8)).isoformat(),
    }

    response = client.get("/patient/2")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Adam",
        "surname": "Kowalski",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=12)).isoformat(),
    }

    response = client.get("/patient/3")
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "name": "Marek11",
        "surname": "Witkowski200",
        "register_date": date.today().isoformat(),
        "vaccination_date": (date.today() + timedelta(days=14)).isoformat(),
    }

    response = client.get("/patient/4")
    assert response.status_code == 404

    response = client.get("/patient/0")
    assert response.status_code == 400
