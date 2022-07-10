from sqlalchemy import create_engine, engine

def get_engine(
    fname: str = './.server',
    db: str = None    
) -> engine.base.Engine:
    with open(fname, 'r') as f:
        for line in f:
            # print(f'{line=}')
            if line[0] == '#': continue

            vals = [s.strip() for s in line.split(':')]
            if vals[0] == 'server': 
                server = vals[1]
                continue
            if vals[0] == 'login': 
                login = vals[1]
                continue
            if vals[0] == 'password':  
                password = vals[1]
                continue
    
    if not (server and login and password):
        raise ValueError("Server access credentials are not valid")

    db_str = f'/{db}' if db else ''
    
    engine = create_engine(
        f'mssql+pyodbc://{login}:{password}@{server}{db_str}'
        f'?driver=ODBC Driver 17 for SQL Server'
        )

    return engine


if __name__ == '__main__':
    eng = get_engine()
    print(type(eng))
    print(eng)