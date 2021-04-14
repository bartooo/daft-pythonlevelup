from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


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
