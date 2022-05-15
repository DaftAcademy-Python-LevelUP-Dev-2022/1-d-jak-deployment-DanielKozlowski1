import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseSettings


class Settings(BaseSettings):
    events_counter: int = 0


class EventCounter:
    received_data: Dict[str, Any]


app = FastAPI()
settings = Settings()


@app.get("/")
def root():
    return {"start": "1970-01-01"}


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


days = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}


@app.get("/day", status_code=200)
def get_day(name: str, number: int):
    if number in days:
        if days.get(number, False) == "name":
            return days[number]
        else:
            return HTTPException(status_code=400, detail="Invalid day!")
    else:
        return HTTPException(status_code=400, detail="Number higher than 7!")


@app.put("/events", status_code=201, response_model=EventCounter)
def put_event(data: EventCounter):

    new_data = data.received_data.copy()
    new_data["name"] = new_data["event"]
    new_data.pop("name")
    new_data["date_added"] = str(datetime.date.today())
    new_data["id"] = settings.events_counter

    settings.events_counter += 1

    return new_data


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

# class HelloResp(BaseModel):
#     msg: str
