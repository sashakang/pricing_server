# tutorial: https://realpython.com/fastapi-python-web-apis/#create-a-first-api
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt, timezone, timedelta

from casts import main as mn


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    print('Got get', dt.now())
    return {"user_id": user_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


@app.put("/put/items/{item_id}")
async def create_item(item_id: str):
    print('Got put', dt.now())
    item = Item(name=item_id, price= 5)
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


if __name__ == '__main__':
    print('Timestamp:', dt.strftime(dt.now(), "%d/%m/%y %H:%M:%S") + "+03:00")
    mn()

    uvicorn.run('pricing_server:app', host='127.0.0.1', port=8080)