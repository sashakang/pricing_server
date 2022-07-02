# tutorial: https://realpython.com/fastapi-python-web-apis/#create-a-first-api
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt, timezone, timedelta
import pandas as pd
from services import get_engine
import os
from casts import main as mn


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI(debug=True)


@app.get("/test")
def testing():
    engine = get_engine('server_credentials')
    punches = pd.read_sql('''
        -- all items
            SELECT
                CAST(items._Fld1527 AS int) AS Артикул
                , items._Description AS Наименование
                , items._Fld36207 AS ДлинаПуансона
                , items._Fld36208 AS ШиринаПуансона
                , items._Fld36209 AS ВысотаПуансона
            FROM _Reference76 AS items
                LEFT JOIN _Reference76 AS categories
                    ON categories._IDRRef = items._ParentIDRRef
            WHERE
                categories._Code = 'ФР-00013807'  -- рабочая форма
                AND CAST(items._Marked AS int) = 0   -- ПометкаУдаления
                AND CAST(items._Fld13793 AS int) = 0   -- Недействителен
                AND CAST(items._Fld36206 AS int) = 1  -- Пуансон
    ''', engine)

    print(punches.head())
    return "testing"


@app.get("/ping")
def pinger():
    stream = os.popen('ping -c 1 ps03.dom.dikart.ru')
    result = stream.read()
    print(result)
    return result
    
    
@app.get("/")
def read_root():
    print('\t', dt.now())
    return {"Hello": "World!"}


@app.get("/users/me")
async def read_user_me():
    print('\t', dt.now())
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    print('\t', dt.now())
    return {"user_id": user_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    print('\t', dt.now())
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    print('\t', dt.now())
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


@app.put("/put/items/{item_id}")
async def create_item(item_id: str):
    print('\t', dt.now())
    item = Item(name=item_id, price= 5)
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


if __name__ == '__main__':
    print('Timestamp:', dt.strftime(dt.now(), "%d/%m/%y %H:%M:%S") + "+03:00")
    mn()

    uvicorn.run('pricing_server:app', host='127.0.0.1', port=8000)