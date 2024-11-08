import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse

def main(params):

    #Connect to DB
    pg_user = params.user
    pg_password  = params.password
    pg_host = params.host
    pg_port = params.port
    pg_db = params.db
    pg_table = params.table
    csv_path = params.csv_path

    #Connection
    engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")
    con = engine.connect()

    try:
            t_start = time()

            #Read data, no iterator batch needed due to size of dataset
            df = pd.read_csv(csv_path, sep=',', header=0, infer_datetime_format=True)
            
            #Load Data to DB
            df.head(0).to_sql(con = con, name = pg_table, if_exists = "replace") #Table Schema
            df.to_sql(con = con, name = pg_table, if_exists = "append")
        
            end_time = time()
            print("New Records Added! {}".format(end_time - t_start))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        engine.dispose() 
        print("All chunks have been processed successfully.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser( description='Data ingest to Olympics Table',)
    parser.add_argument('--user', help="Database User")      # option that takes a value
    parser.add_argument('--password', help="Database Password")      # option that takes a value
    parser.add_argument('--host', help="Database Host")      # option that takes a value
    parser.add_argument('--port', help="Database Port")      # option that takes a value
    parser.add_argument('--db', help="Database Name")      # option that takes a value
    parser.add_argument('--table', help="Database Table")      # option that takes a value
    parser.add_argument('--csv_path', help="CSV Path")      # option that takes a value

    params = parser.parse_args()

    main(params)