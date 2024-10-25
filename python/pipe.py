import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import time



class ELTPipeline:

    def __init__(self, dbpath = 'olympicsdata.ddb'):
        self.conn = duckdb.connect(dbpath)
        print(f"Connected to {dbpath}")   

    def extract(self, table_name = 'ol_econ', csv_path = 'olympics-economics.csv'):
        print(f"Extracting data from {csv_path}...")

        self.conn.execute(f'''
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv('{csv_path}')
            WHERE gdp_year = 2023
            ORDER BY total DESC;
        ''')

        df = self.conn.execute(f'''
            SELECT * FROM {table_name};
        ''').fetch_df()

        end_time = time.time()

        print(f"Data extracted successfully from {csv_path} into table {table_name}")
        return df

    def review(self, table_name, df):
        print(f"Successfully loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    
    pipeline = ELTPipeline()

    df = pipeline.extract()

    pipeline.review('ol_econ', df)

    


  