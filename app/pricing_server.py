# tutorial: https://realpython.com/fastapi-python-web-apis/#create-a-first-api
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt
import pandas as pd
from services import get_engine
import os
from casts import main as main_
from sqlalchemy import create_engine
from spartak_report import write_spartak_data


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI(debug=True)


@app.get("/spartak")
def write_spartak():
    write_spartak_data()
    print(dt.strftime(dt.now(), "%d/%m/%y %H:%M:%S") + "+03:00")
    return "Spartak data been written successfully."

@app.get("/test")
def testing():
    print('Got TEST')
    print(f'{os.getcwd()=}')

    engine = get_engine(
        fname='../credentials/.prod_unf'
    )
    print(engine)
    punches = pd.read_sql('''
-- order tables
SELECT 
--    CAST(DATEADD([YEAR], -2000, orders._Date_Time) AS date) AS ДатаЗаказа
    numbers._Fld16427 AS НомерЗаказа
--    , price_types._Description AS ВидЦен
--    , orders._Fld16954 AS СкидкаСуммой
   , tables._Fld35933 AS Этап
   , room._Description AS Помещение
    , tables._LineNo3639 AS СтрокаЗП
   , complex_specs._Description AS spec
    , tech._Description AS tech
   , IIF(supercategories._Description IS NULL, categories._Description, supercategories._Description) AS category
   , IIF(supercategories._Description IS NULL, NULL, categories._Description) AS subcategory
   , CAST(items._Fld1527 AS int) AS Артикул
    , items._Description AS Номенклатура
        , CASE
            WHEN CAST(items._Fld17384RRef AS uniqueidentifier) = 'B0097DA4-D6EA-4FD9-4102-3C68406126E1' THEN 'Гипс Г-16'
            WHEN CAST(items._Fld17384RRef AS uniqueidentifier) = '9D4E9883-5C68-0F52-47FC-282070B93A8B' THEN 'Полиуретан'
            WHEN CAST(items._Fld17384RRef AS uniqueidentifier) = 'A8714BB0-32CB-87EC-49F0-F46150272118' THEN 'Стеклофиброгипс'
            ELSE NULL
        END AS Материал        
        , units._Description AS unit
        , CAST(items._Fld16170 AS int) AS Высота
        , CAST(items._Fld16171 AS int) AS Ширина
        , CAST(items._Fld17891 AS int) AS Глубина
        , CAST(items._Fld17892 AS int) AS Диаметр
        , items._Fld17923 AS ДлинаL
        , tables._Fld16185 AS Радиус
        , CAST(tables._Fld16186 AS int) AS Лекало
        , tables._Fld16394 AS ВнутреннийУгол
        , tables._Fld16395 AS ВнешнийУгол
        , tables._Fld16396 AS ВертикальныйУгол
        , tables._Fld16188 AS ВсегоУглов
        , CAST(tables._Fld16439 AS int) AS ЦенаИзмененаВручную
    , CASE
      WHEN CAST(tables._Fld16465RRef AS uniqueidentifier) = '00000000-0000-0000-0000-000000000000' THEN 1   -- DEFAULT
      WHEN CAST(tables._Fld16465RRef AS uniqueidentifier) = '3C6931AC-DBF0-99B5-4936-2D3F3B3EE6F3' THEN 1   -- EQUAL
      WHEN CAST(tables._Fld16465RRef AS uniqueidentifier) = 'E1988ABF-4ECD-C8A1-454C-238E8BA7A210' THEN 1   -- PLUS
      WHEN CAST(tables._Fld16465RRef AS uniqueidentifier) = '752B2296-D11C-3E12-4106-E40E1A14C942' THEN -1  -- MINUS
      ELSE 999999
    END AS Корректировка
        , tables._Fld35429 AS КоличествоЧистое
    , tables._Fld3644 AS Количество
        , tables._Fld3648 AS Цена
    , tables._Fld3650 AS Сумма
    , tables.[_Fld16385] AS СуммаБезСкидок
--    , CAST(extra._Fld17380 AS int) AS ТолькоМонтаж
--    , orders._Fld16362 AS СкидкаМонтажПроцент
    , CAST(DATEADD([YEAR], -2000, tables._Fld16364) AS date) AS ДатаОтгрузки
        , IIF(CAST(tables._Fld17386 AS int) = 1 OR CAST(items._Fld35670 AS int) = 1, 1, 0) AS Врезное
        , IIF(CAST(tables._Fld35724 AS int) = 1 OR CAST(items._Fld35696 AS int) = 1, 1, 0) AS Вентиляционный
--    , b24link.[_Fld35487] AS b24Id
FROM _Document164_VT3638X1 AS tables
    LEFT JOIN _Reference76 AS items ON items._IDRRef = tables._Fld3640RRef
    LEFT JOIN _Reference64 as units ON items._Fld1529RRef = units._IDRRef
    LEFT JOIN _Reference76 AS categories ON categories._IDRRef = items._ParentIDRRef
    LEFT JOIN _Reference76 AS supercategories ON supercategories._IDRRef = categories._ParentIDRRef
    LEFT JOIN _Reference79 as tech ON items._Fld1533RRef = tech._IDRRef
    LEFT JOIN _Document164X1 AS orders ON tables._Document164_IDRRef = orders._IDRRef
--    LEFT JOIN _Reference36 AS price_types ON price_types._IDRRef = orders._Fld3599RRef    
    LEFT JOIN _InfoRg16413 as numbers on numbers._Fld16426RRef = orders._idrref
--    LEFT JOIN _Reference102 AS projects ON projects._IDRRef = orders._Fld3613RRef
    LEFT JOIN _Reference16143 AS room ON room._IDRRef = tables._Fld16181RRef
    LEFT JOIN _Reference16144 AS complex_specs ON tables._Fld16182RRef = complex_specs._IDRRef
WHERE 
--    tech._Description IN ('Отливка', 'Протяжка', 'Отливная тяга резина', 'Отливная тяга пластик', 'Фиброгипс')
--        numbers._Fld16427 IS NOT NULL 
--    AND numbers._Fld16427 <> '' -- номер заказа
--        AND projects._Code = 15414
    numbers._Fld16427 LIKE '13925/12/%' AND
    CAST(orders._Posted AS int) = 1
--    AND items._Description LIKE 'и%'
    AND items._Description IS NOT NULL
    AND CAST(DATEADD([YEAR], -2000, orders._Date_Time) AS date) > '2021-01-01'
--    AND items._Fld1527 = '200031'   -- Артикул
--ORDER BY numbers._Fld16427, tables._LineNo3639  -- номер заказа, номер строки
    ''', engine)

    print(punches.iloc[:5, :5])
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
    main_()

    uvicorn.run('pricing_server:app', host='127.0.0.1', reload=False)