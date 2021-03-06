from fastapi import FastAPI, Request, Response, Depends, HTTPException, status, Cookie
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import hashlib
import secrets
from typing import Optional
from datetime import date, datetime, timedelta
from routers import database, views

app = FastAPI()
app.counter = 0
app.patient_counter = 0
app.db = dict()
app.secret_key = "very secret key"
app.session_cookie = []
app.session_token = []
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

app.include_router(database.router)
app.include_router(views.router)


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
    month = today.month if today.month >= 10 else f"0{today.month}"
    day = today.day if today.day >= 10 else f"0{today.day}"
    return templates.TemplateResponse(
        "hello.html.j2",
        {"request": request, "YYYY": today.year, "MM": month, "DD": day},
    )


def compare_username(given, correct):
    correct_username = secrets.compare_digest(given, correct)
    return correct_username


def compare_passwd(given, correct):
    correct_password = secrets.compare_digest(given, correct)
    return correct_password


def check_passes(username, passwd):
    if not (username and passwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def generate_session(username, passwd):
    session_token = hashlib.sha256(
        f"{username}{passwd}{app.secret_key}{app.counter}".encode()
    ).hexdigest()
    return session_token


def select_container(is_cookie):
    if is_cookie:
        container = app.session_cookie
    else:
        container = app.session_token
    return container


def store_session(session, is_cookie):
    container = select_container(is_cookie)

    if len(container) >= 3:
        del container[0]

    container.append(session)


@app.post("/login_session")
def login_session(
    response: Response, credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = compare_username(credentials.username, "4dm1n")
    correct_password = compare_passwd(credentials.password, "NotSoSecurePa$$")
    check_passes(correct_username, correct_password)
    app.counter += 1
    session_token = generate_session(credentials.username, credentials.password)
    response.set_cookie(key="session_token", value=session_token)
    store_session(session_token, True)
    response.status_code = 201


@app.post("/login_token")
def login_token(
    response: Response, credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = compare_username(credentials.username, "4dm1n")
    correct_password = compare_passwd(credentials.password, "NotSoSecurePa$$")
    check_passes(correct_username, correct_password)
    app.counter += 1
    session_token = generate_session(credentials.username, credentials.password)
    response.status_code = 201
    store_session(session_token, False)
    return {"token": session_token}


def generate_html_response(request: Request, h1: str):
    return templates.TemplateResponse(
        "mess.html.j2",
        {"request": request, "h1": h1},
    )


def generate_json_response(msg: str):
    msg = {"message": msg}
    return JSONResponse(content=msg, status_code=200)


def generate_plain_response(msg: str):
    return PlainTextResponse(content=msg, status_code=200)


def check_session_token(session_token, is_cookie):
    if is_cookie:
        container = app.session_cookie
    else:
        container = app.session_token

    if len(container) == 0 or session_token is None or session_token not in container:
        raise HTTPException(status_code=401, detail="Unathorised")


def generate_response(format, request, msg):
    if format == "json":
        return generate_json_response(msg)
    elif format == "html":
        return generate_html_response(request, msg)
    else:
        return generate_plain_response(msg)


def del_session_token(session_token, is_cookie):
    container = select_container(is_cookie)
    index = container.index(session_token)
    del container[index]


@app.get("/welcome_session")
def welcome_session(
    request: Request, session_token: str = Cookie(None), format: Optional[str] = None
):

    check_session_token(session_token, True)
    return generate_response(format, request, "Welcome!")


@app.get("/welcome_token")
def welcome_token(
    request: Request, token: Optional[str] = None, format: Optional[str] = None
):
    check_session_token(token, False)
    return generate_response(format, request, "Welcome!")


@app.delete("/logout_session")
def logout_session(
    request: Request, session_token: str = Cookie(None), format: Optional[str] = None
):
    check_session_token(session_token, True)
    del_session_token(session_token, True)
    return RedirectResponse(
        url=f"/logged_out?format={format}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.delete("/logout_token")
def logout_token(
    request: Request, token: Optional[str] = None, format: Optional[str] = None
):
    check_session_token(token, False)
    del_session_token(token, False)
    return RedirectResponse(
        url=f"/logged_out?format={format}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/logged_out")
def logged_out(request: Request, format: Optional[str] = None):
    return generate_response(format, request, "Logged out!")
