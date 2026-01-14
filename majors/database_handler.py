import sqlalchemy as sa
import pandas as pd
from sqlalchemy import text

class DatabaseHandler:
    def __init__(self, db_params):
        # Construct the database connection URI
        self.db_uri = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        
        try:
            # Create SQLAlchemy engine
            self.engine = sa.create_engine(self.db_uri)
            
            # Test the connection
            with self.engine.connect() as connection:
                print("Database connected successfully!")
        
        except Exception as e:
            print(f"Database connection error: {e}")
            self.engine = None
    
    def query(self, sql_query):
        if not self.engine:
            raise ConnectionError("Database connection for query is not established.")
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql_query))
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            print(f"Query execution error: {e}")
            raise
    
    def query_scalar(self, sql_query):
        """
        Execute a query and return a single scalar value.
        
        :param sql_query: The SQL query string.
        :return: A scalar value (e.g., a single number).
        """
        if not self.engine:
            raise ConnectionError("Database connection for query_scalar is not established.")
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql_query)).scalar()
                return result
        except Exception as e:
            print(f"Scalar query execution error: {e}")
            raise


    def get_connection(self):
        return self.engine
    
    def close(self):
        if hasattr(self, 'engine') and self.engine:
            # Dispose of the engine
            self.engine.dispose()
            print("Database connection closed.")