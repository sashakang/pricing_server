# tutorial: https://realpython.com/fastapi-python-web-apis/#create-a-first-api
# setup PyCharm: https://stackoverflow.com/questions/62856818/how-can-i-run-the-fast-api-server-using-pycharm
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt, timezone, timedelta


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
    print(dt.now())
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


@app.put("/put/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


if __name__ == '__main__':
    print('Timestamp:', dt.strftime(dt.now(), "%d/%m/%y %H:%M:%S") + "+03:00")

    uvicorn.run(app)