import pandas as pd
import duckdb 
from sqlalchemy import create_engine


def query_postgre_duck():
    #Connection parameters
    pg_user = 'root'
    pg_password = 'root'
    pg_host = 'pgdatabase'
    pg_port = '5432'
    pg_db = 'olympics24db'

    try:
        #Postgresql connection string
        pg_connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

        #Cretae Duckdb connection
        duck_conn = duckdb.connect()

        #Install and load Postgresql extension for duckdb
        duck_conn.install_extension("postgres_scanner")
        duck_conn.load_extension("postgres_scanner")

        #Attach to Postgresql db
        duck_conn.execute(f"""
        ATTACH '{pg_connection_string}' AS olympics24db (TYPE postgres);
        """)

        #list all tables (test query)
        tables = duck_conn.execute("""
        SELECT * FROM olympics24db.information_schema.tables
        WHERE table_schema = 'public';        
        """).fetchdf()

        print("\nAvailable tables:")
        print(tables)

        # target data (test query)
        data = duck_conn.execute("""
        SELECT * FROM olympics24db.public.olyecon LIMIT 5;
        """).fetchdf()
        print("\nSample data from olyecon table:")
        print(data)
    
    except Exception as e:
        print(f"An error occurred:{e}")
    finally:
        duck_conn.close()

if __name__ == "__main__":
    query_postgre_duck()

