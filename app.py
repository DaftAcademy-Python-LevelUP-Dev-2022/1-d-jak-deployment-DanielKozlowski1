import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    events_counter: int = 0


class EventCounterRq(BaseModel):
    event: str
    date: str


class EventCounterRs(BaseModel):
    name: str
    date: str
    id: int
    date_added: str


class EventsListRs(BaseModel):
    fin_list: List[Dict[str, Any]]


app = FastAPI()
settings = Settings()

events: List[Dict[str, Any]] = []


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


@app.get("/day/", status_code=200)
def get_day(name: str, number: int):
    if number in days:
        if days.get(number, False) == name:
            return days[number]
        else:
            raise HTTPException(status_code=400, detail="Invalid day!")
    else:
        raise HTTPException(status_code=400, detail="Number higher than 7!")


@app.put("/events", status_code=200, response_model=EventCounterRs)
def put_event(data: EventCounterRq):

    name = data.event
    date = data.date
    id = settings.events_counter
    settings.events_counter += 1
    date_added = str(datetime.date.today())
    fin_dict = {"name": name, "date": date, "id": id, "date_added": date_added}
    events.append(fin_dict)

    return EventCounterRs(**fin_dict)


@app.get("/event/{date}", status_code=200, response_model=EventsListRs)
def get_event(date: str):

    try:
        _ = (datetime.datetime.strptime(date, "YYYY-MM-DD"),)
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")

    final_events: List[Dict[str, Any]] = []

    for event in events:
        if event["date"] == date:
            final_events.append(event)

    if len(final_events) > 0:
        return EventsListRs(
            fin_list=[EventCounterRs(**d) for d in final_events]
        )
    else:
        raise HTTPException(status_code=404, detail="Didn't find any data")


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
