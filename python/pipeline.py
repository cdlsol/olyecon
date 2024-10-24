import pandas as pd
import duckdb 

class ETLPipeline:
    def __init__(self, db_path = 'analytics.ddb'):
        self.conn = duckdb.connect(db_path)

    def exctract(self, csv_path):
        print(f"Extracting data from {csv_path}")
        return pd.read_csv(csv_path)

    def transform(self, df):
        ... #pending transformation specs
        print("Transforming Data")
        return transformed_df

    def load(self, df, table_name):
        print(f"Loading data into table: {table_name}")

        column_schema = self._generate_schema(df)
        create_table_sql = f""" 
            CREATE TABLE IF NOT EXISTS {table_name} (
            {column_schema})
        """
        self.conn.execute(create_table_sql)

        # Load the data
        self.conn.register('temp_df', df)
        self.conn.execute(f"""
            INSERT INTO {table_name}
            SELECT * FROM temp_df
        """)

        print(f"Successfully loaded {len(df)} rows into {table_name}")
    

    def _generate_schema(self, df):
        """Generate SQL schema from DataFrame"""
        type_mapping = {
            'object': 'VARCHAR',
            'int64': 'INTEGER',
            'float64': 'DOUBLE',
            'datetime64[ns]': 'TIMESTAMP',
            'bool': 'BOOLEAN'
        }
        
        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = type_mapping.get(str(dtype), 'VARCHAR')
            columns.append(f"{col} {sql_type}")
            
        return ",\n    ".join(columns)

if __name__ == "__main__":
    # Initialize pipeline
    pipeline = ETLPipeline()
    
    # Run ETL process
    df = pipeline.extract('olympics-economics.csv"')
    transformed_df = pipeline.transform(df)
    pipeline.load(transformed_df, 'analytics_table')
    
    # Verify the data
    result = pipeline.conn.execute("SELECT COUNT(*) FROM analytics_table").fetchone()
    print(f"Total rows in database: {result[0]}")


    
        