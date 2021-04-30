from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import hashlib
from typing import Optional
from datetime import date, datetime, timedelta

app = FastAPI()
app.counter = 0
app.patient_counter = 0
app.db = dict()
templates = Jinja2Templates(directory="templates")


class HelloResp(BaseModel):
    msg: str


class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    surname: str
    register_date: Optional[str] = None
    vaccination_date: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
async def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.api_route("/method", methods=["GET", "POST", "DELETE", "OPTIONS", "PUT"])
def method(request: Request, response: Response):
    if request.method == "POST":
        response.status_code = 201
    else:
        response.status_code = 200
    return {"method": request.method}


@app.get("/auth/")
async def auth(
    response: Response,
    password: Optional[str] = None,
    password_hash: Optional[str] = None,
):
    if (
        password is None
        or password_hash is None
        or password == ""
        or password_hash == ""
    ):
        response.status_code = 401
        return
    hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
    if hash == password_hash:
        response.status_code = 204
    else:
        response.status_code = 401


@app.post("/register/")
async def register(response: Response, patient: Patient):
    app.patient_counter += 1
    patient.id = app.patient_counter
    patient.register_date = date.today().isoformat()
    letters_name = len([c for c in patient.name if c.isalpha()])
    letters_surname = len([c for c in patient.surname if c.isalpha()])
    vaccination_date = date.today() + timedelta(days=letters_name + letters_surname)
    patient.vaccination_date = vaccination_date.isoformat()
    app.db[patient.id] = patient.dict()
    response.status_code = 201
    return patient.dict()


@app.get("/patient/{id}")
async def patient(response: Response, id: int):
    if id in app.db.keys():
        response.status_code = 200
        return app.db[id]
    else:
        if id < 1:
            response.status_code = 400
        else:
            response.status_code = 404


@app.get("/hello")
def hello(request: Request):
    today = datetime.today()
    return templates.TemplateResponse(
        "hello.html.j2",
        {"request": request, "YYYY": today.year, "MM": today.month, "DD": today.day},
    )
