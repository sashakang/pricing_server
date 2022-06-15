import pandas as pd
import sqlalchemy
# import time
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# print server version
# import pyodbc
# for driver in pyodbc.drivers():
#      print(driver)

def main():
    print(f'{os.getcwd()=}')

    try:
        fname = 'write.txt'
        for root, dirs, files in os.walk('..'):
            if fname in files:
                path = os.path.join(root, fname)
                print(path)
        with open(path, 'w') as f:
            f.write('update1')
        print('Write successful')
    except:
        print("Can't write")

    # time.sleep(60)

    try:
        fname = 'server.txt'
        for root, dirs, files in os.walk('..'):
            if fname in files:
                path = os.path.join(root, fname)
                print(path)
        with open(path, 'r') as f:
            server = f.readline().split()[1]
            login = f.readline().split()[1]
            password = f.readline().split()[1]
            print(f'{server=}\n{login=}\n{password=}')

        engine = sqlalchemy.create_engine(
            f'mssql+pyodbc://{login}:{password}@{server}/'
            'PROD_UNF?driver=ODBC Driver 17 for SQL Server'
        )

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

    except:
        print('`server.txt` not found')

# time.sleep(90)

if __name__ == '__main__':
    main()