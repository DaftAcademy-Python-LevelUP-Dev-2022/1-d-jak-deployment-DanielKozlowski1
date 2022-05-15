from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"start": "1970-01-01"}


class HelloResp(BaseModel):
    msg: str


@app.post(path="/method", status_code=201)
def get_post():
    return {"method": "POST"}


@app.api_route(
    path="/method",
    methods=["GET", "PUT", "OPTIONS", "DELETE"],
    status_code=200,
)
async def get_methods(request: Request):
    return {"method": request.method}


# @app.get("/hello/{name}", response_model=HelloResp)
# def read_item(name: str):
#     return HelloResp(msg=f"Hello {name}")


# class GiveMeSomethingRq(BaseModel):
#     first_key: str


# class GiveMeSomethingResp(BaseModel):
#     received: Dict
#     constant_data: str = "python jest super"


# @app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
# def receive_something(rq: GiveMeSomethingRq):
#     return GiveMeSomethingResp(received=rq.dict())
