import pandas as pd
import sqlalchemy
from services import get_engine
from datetime import datetime as dt
import time

def write_spartak_data():

    unf_engine = get_engine('../credentials/.prod_unf')
    analytics_engine = get_engine('../credentials/.server_analytics')

    project = '13925/%'

    query_order_tables = f'''
    -- order tables
    SELECT 
        CAST(DATEADD([YEAR], -2000, orders._Date_Time) AS date) AS ДатаЗаказа
        , numbers._Fld16427 AS НомерЗаказа
        , tables._Fld35933 AS Этап
        , room._Description AS Помещение
        , tables._LineNo3639 AS СтрокаЗП
        , complex_specs._Description AS spec
        , CAST(complex_specs._IDRRef AS uniqueidentifier) AS specId
        , tech._Description AS tech
        , IIF(supercategories._Description IS NULL, categories._Description, supercategories._Description) AS category
        , IIF(supercategories._Description IS NULL, NULL, categories._Description) AS subcategory
        , items._Fld1527 AS Артикул
        , items._Description AS Номенклатура
        , CAST(items._IDRRef AS uniqueidentifier) AS itemId
        , tables._Fld35429 AS КоличествоЧистое
        , tables._Fld3644 AS Количество
        , units._Description AS еи
        , tables._Fld3648 AS Цена
        , tables._Fld3650 AS Сумма
        , tables._Fld16185 AS Радиус
        , CAST(tables._Fld16186 AS int) AS Лекало
        , batch.[_Description] AS Партия
        , CAST(tables.[_Fld3643RRef] AS uniqueidentifier) AS ПартияId    
    FROM _Document164_VT3638X1 AS tables
        LEFT JOIN _Reference76 AS items ON items._IDRRef = tables._Fld3640RRef
        LEFT JOIN _Reference64 as units ON items._Fld1529RRef = units._IDRRef
        LEFT JOIN _Reference76 AS categories ON categories._IDRRef = items._ParentIDRRef
        LEFT JOIN _Reference76 AS supercategories ON supercategories._IDRRef = categories._ParentIDRRef
        LEFT JOIN _Reference79 as tech ON items._Fld1533RRef = tech._IDRRef
        LEFT JOIN _Document164X1 AS orders ON tables._Document164_IDRRef = orders._IDRRef
        LEFT JOIN _InfoRg16413 as numbers on numbers._Fld16426RRef = orders._idrref
        LEFT JOIN _Reference16143 AS room ON room._IDRRef = tables._Fld16181RRef
        LEFT JOIN _Reference16144 AS complex_specs ON tables._Fld16182RRef = complex_specs._IDRRef
        LEFT JOIN _Reference89 AS batch ON batch.[_IDRRef] = tables.[_Fld3643RRef]
    WHERE 
        numbers._Fld16427 LIKE '{project}'
        AND CAST(orders._Posted AS int) = 1
        AND CAST(DATEADD([YEAR], -2000, orders._Date_Time) AS date) > '2022-01-01'
    ORDER BY numbers._Fld16427, tables._LineNo3639	-- номер заказа, номер строки
    '''

    order_tables = pd.read_sql(query_order_tables, unf_engine)

    int_cols = ["СтрокаЗП", "Этап", "Радиус"]
    for col in int_cols:
        order_tables[col] = order_tables[col].astype(int)
    
    tables_w_specs = order_tables[order_tables.spec.notnull()]
    spec_names = tables_w_specs.spec.unique()
    query_specs = f'''
    -- complex_specs.sql
    SELECT specs._Description AS Спецификация
        , CAST(specs.[_IDRRef] AS uniqueidentifier) AS specId
        , CAST(parent._Fld1527 AS int) AS артикулРодитель
        , parent._Description AS Родитель
        , parent_tech._Description AS родительТехнология
        , parent_cat._Description AS родительКатегория
        , CAST(component._Fld1527 AS int) AS артикулКомпонент
        , component._Description AS Компонент
        , CAST(component.[_IDRRef] AS uniqueidentifier) AS componentId
        , component_tech._Description AS компонентТехнология
        , components_list._Fld16192 AS количество
        , components_list._Fld16163 AS радиус
        , CAST(components_list._Fld16164 AS int) AS лекало
        , IIF(component_tech._Description IN ('Модельные работы', 'Формовочные работы'), components_list._Fld36159, NULL) AS тариф
        , IIF(component_tech._Description IN ('Модельные работы', 'Формовочные работы'), components_list._Fld36160, NULL) AS цена
    FROM _Reference16144 AS specs
        LEFT JOIN _Reference76 AS parent ON specs._Fld16369RRef = parent._IDRRef
        LEFT JOIN _Reference79 AS parent_tech ON parent._Fld1533RRef = parent_tech._IDRRef
        LEFT JOIN _Reference76 AS parent_cat ON parent._ParentIDRRef = parent_cat._IDRRef
        LEFT JOIN _Reference16144_VT16155 AS components_list ON components_list._Reference16144_IDRRef  = specs._IDRRef
        LEFT JOIN _Reference76 AS component ON components_list._Fld16157_RRRef = component._IDRRef
        LEFT JOIN _Reference79 AS component_tech ON component._Fld1533RRef = component_tech._IDRRef
    WHERE 
        CAST(specs._Marked AS int) = 0
        AND CAST(parent._Fld13793 AS int) = 0    -- действительный продукт
        AND CAST(parent._Marked AS int) = 0
        AND specs._Description IN ('{"', '".join(spec_names)}')
    '''

    specs = pd.read_sql(query_specs, unf_engine)

    query_prod_orders = f'''
    -- prod_tables.sql
    SELECT 
        numbers._Fld16427 AS НомерЗП
        , CAST(orders._IDRRef AS uniqueidentifier) AS ЗПId
        , parent_prod_order.[_Number] AS parentЗНП
        , CAST(parent_prod_order.[_IDRRef] AS uniqueidentifier) AS parentЗНПId
        , prod_order._Number AS НомерЗнП
        , CAST(prod_order._IDRRef AS uniqueidentifier) AS ЗнПId
        , DATEADD([YEAR], -2000, prod_order._Date_Time) AS ДатаЗнП
        , status._Description AS СтатусЗнП
        , prod_tables.[_LineNo3563] AS СтрокаЗнП
        , item._Description AS Номенклатура
        , item.[_Fld1527] AS Артикул
        , units.[_Description] AS еи
        , parent.[_Description] AS Владелец
        , parent._Fld1527 AS ВладелецАртикул
        , prod_tables._Fld36215 AS Тариф
        , prod_tables._Fld3567 AS Количество
        , tech._Description AS Технология
        , batch.[_Description] AS Партия
        , CAST(batch.[_IDRRef] AS uniqueidentifier) AS ПартияId
        FROM _Document163 AS prod_order
        JOIN _Reference117 AS status ON prod_order._Fld3556RRef = status._IDRRef
        JOIN _Document163_VT3562 AS prod_tables ON prod_order._IDRRef = prod_tables._Document163_IDRRef
        JOIN _Reference76 AS item ON item._IDRRef = prod_tables._Fld3564RRef
        JOIN _Reference79 as tech ON item._Fld1533RRef = tech._IDRRef
        LEFT JOIN _Reference64 as units ON item._Fld1529RRef = units._IDRRef    
        LEFT JOIN _Reference76 AS parent ON prod_tables._Fld33461RRef = parent.[_IDRRef] 
        LEFT JOIN [_Document164X1] AS orders ON orders._IDRRef = prod_order._Fld3543RRef
        LEFT JOIN _InfoRg16413 as numbers on numbers._Fld16426RRef = orders._IDRRef
        LEFT JOIN _Document163 AS parent_prod_order ON prod_order.[_Fld3555RRef] = parent_prod_order._IDRRef
        LEFT JOIN _Reference89 AS batch ON prod_tables.[_Fld16259RRef] = batch.[_IDRRef]
    WHERE 
        numbers._Fld16427 LIKE '13925/%'  -- parent НомерЗП
        AND CAST(prod_order._Posted AS int) = 1
    ORDER BY prod_order._Date_Time DESC
    '''

    prod_orders_tbl = pd.read_sql(query_prod_orders, unf_engine)
    prod_orders_tbl.СтрокаЗнП = prod_orders_tbl.СтрокаЗнП.apply(int)

    prod_order_ids = "', '".join(prod_orders_tbl.ЗнПId.unique())

    query_jobs = f'''
    DECLARE @productionRefType int = 207;  -- reference type for 'productions'
    -- @job_ticket_tables.sql
    -- pulls & castings shops pay monthly
    SELECT
        CAST(DATEADD([YEAR], -2000, ticket._Date_Time) AS date) AS date,
        ticket._Number AS doc,
        tbl._LineNo5263 AS row_no,
        prod_order.[_Number] AS prodOrderN,
        CAST(DATEADD([YEAR], -2000, prod_order.[_Date_Time]) AS date) AS prodOrderDate,
        CAST(prod_order.[_IDRRef] AS uniqueidentifier) AS prodOrderId,
        CAST(item._Fld1527 AS int) AS item_id,
        item._Description AS item,
        tbl._Fld5271 AS quantity,
        units.[_Description] AS unit,
        tbl.[_Fld5273] AS rate,
        CAST(tbl._Fld5275 AS float) AS pay,
        (
            CASE
            WHEN _Fld16365_RTRef = @productionRefType 
            THEN CAST(DATEADD([YEAR], -2000, production._Date_Time) AS date) 
            ELSE NULL
            END
        ) AS productionDate,
        (
            CASE
            WHEN @productionRefType = _Fld16365_RTRef  THEN production._Number
            ELSE NULL
            END
        ) AS productionNo,
        (
            CASE
            WHEN @productionRefType = _Fld16365_RTRef  
                THEN CAST(production._IDRRef AS uniqueidentifier)
            ELSE NULL
            END
        ) AS productionId,
        CAST(batch.[_IDRRef] AS uniqueidentifier) AS batchId,
        batch._Description AS batch
    FROM 
        _Document209 ticket 
        LEFT JOIN _Document209_VT5262 tbl ON ticket._IDRRef = tbl._Document209_IDRRef
        LEFT JOIN _Reference76 item ON tbl._Fld5266RRef = item._IDRRef
        LEFT JOIN _Reference64 as units ON item._Fld1529RRef = units._IDRRef    
        LEFT JOIN _Reference79 tech ON tech._IDRRef = item._Fld1533RRef
        LEFT JOIN _Document163 prod_order ON prod_order._IDRRef = ticket._Fld16366RRef
        LEFT JOIN _Document207 production ON ticket._Fld16365_RRRef = production._IDRRef
        LEFT JOIN _Reference89 AS batch ON batch._IDRRef = tbl._Fld5276RRef
    WHERE 
        CAST(ticket._Posted AS int) = 1
        AND CAST(item._Fld1527 AS int) > 0     -- item_id
        AND CAST(prod_order.[_IDRRef] AS uniqueidentifier) IN ('{prod_order_ids}')
    '''

    jobs = pd.read_sql(query_jobs, unf_engine)
    jobs.row_no = jobs.row_no.astype(int)

    df = order_tables[order_tables.НомерЗаказа.str.startswith('13925/13/')]

    df = df[[
        'СтрокаЗП',
        'spec',
        'specId',
        'tech',
        'Артикул',
        'itemId',
        'Номенклатура',
        'Количество',
        'еи',
        'Партия',
        'ПартияId'
    ]]

    # add budgeted rate
    df = df.merge(
        specs[['specId', 'componentId', 'тариф']], 
        how='left', 
        left_on=['specId', 'itemId'],
        right_on=['specId', 'componentId']
    ).drop(columns='componentId')

    df['budget'] = df.apply(lambda r: r.Количество * r.тариф, axis=1)

    direct_subordinates = prod_orders_tbl[
        prod_orders_tbl.parentЗНПId.isnull()
        & (prod_orders_tbl.НомерЗП.str.startswith('13925/13/'))
    ]

    df = df.merge(
        direct_subordinates[[
            "ПартияId", 
            "НомерЗнП",
            "ЗнПId",
            "СтатусЗнП", 
            "СтрокаЗнП",
            "Количество", 
            "Тариф"
            ]], 
        how='left', 
        on='ПартияId',
        suffixes=['', 'ЗнП']
    )

    df.rename(columns={"Тариф": "ТарифЗнП"}, inplace=True)
    df['Плановая плата'] = df.apply(lambda r: r.КоличествоЗнП * r.ТарифЗнП, axis = 1)


    jobs_grouped = jobs.groupby(
        ['batch', 'batchId', 'item_id', 'item', 'unit']
        ).agg(sum)[['quantity', 'pay']].reset_index()

    jobs_grouped['rate'] = jobs_grouped.apply(lambda r: r.pay / r.quantity, axis=1)

    df = df.merge(
        jobs_grouped[['batchId', 'quantity', 'rate', 'pay']], 
        how='left',
        left_on='ПартияId',
        right_on='batchId'
        )

    timestamp = time.strftime('%d.%m.%y %H:%M:%S', time.gmtime(time.time())) 

    df['timestamp'] = timestamp

    df.to_sql(
        name='spartak',
        con=analytics_engine,
        if_exists='replace',
        index=False,
        dtype={
            'timestamp': sqlalchemy.DateTime
        }
    )
    
    
if __name__ == '__main__':
    write_spartak_data()