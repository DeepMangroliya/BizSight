# import os
# from typing import Optional
# import pandas as pd
# from dotenv import load_dotenv
# from pathlib import Path
# from sqlalchemy import create_engine

# # Load environment variables from the .env file in the project root
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# def run_sql_query_from_file(file_path: Path, database: str) -> Optional[pd.DataFrame]:
#     """
#     Executes a SQL query from a .sql file using SQLAlchemy engine and returns the result as a DataFrame.

#     Args:
#         file_path : Path
#             Path to the SQL file.
#         database : str
#             Name of the database to connect to.

#     Returns: 
#         Optional[pd.DataFrame] : 
#             Query result as a DataFrame if successful, else None.
#     """
#     user = os.getenv('USER') or 'root'
#     password = os.getenv('PASSWORD')
#     host = os.getenv('HOST')

#     connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
#     engine = create_engine(connection_string)

#     try:
#         with open(file_path, 'r') as f:
#             query = f.read()

#         df = pd.read_sql(query, engine)
#         print(f"✅ Query executed successfully. {len(df)} rows retrieved.")
#         return df

#     except FileNotFoundError:
#         print(f"❌ Query file not found: {file_path}")
#     except Exception as e:
#         print(f"❌ Error executing query from file: {e}")

#     return None

# def process() -> None:
#     """
#     Runs a SQL query from file, loads data, and returns the DataFrame.

#     Returns:
#         None
#     """
#     file_path = PROJECT_ROOT / "src" / "query.sql"
#     database = "refined"  # Ensure this matches your actual DB name

#     data = run_sql_query_from_file(file_path=file_path, database=database)
#     return data

# if __name__ == "__main__":
#     process()

# src/data_analysis_ext.py

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
# load_dotenv(Path('.env'))

# def get_engine(database: str):
#     """
#     Creates and returns a SQLAlchemy engine for the given database using
#     credentials from the .env file.
#     """
#     user = os.getenv("USER")
#     password = os.getenv("PASSWORD")
#     host = os.getenv("HOST")
#     port = os.getenv("PORT", "3306")  # default MySQL port if not in .env

#     connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
#     engine = create_engine(connection_string)
#     return engine

def get_engine(database: str):
    """
    Creates and returns a SQLAlchemy engine for the given database using
    credentials from the .env file.
    """
    user = os.getenv("USER") or "root"
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT", "3306")  # Default MySQL port

    if not host:
        raise ValueError("❌ HOST is missing in .env file or not loaded properly.")

    connection_string = f"mysql+pymysql://root:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine

def run_sql_query_from_file(file_path: str, database: str) -> pd.DataFrame:
    """
    Reads an SQL query from a file and executes it against the specified database.

    Args:
        file_path (str): Path to the SQL file.
        database (str): Database name.

    Returns:
        pd.DataFrame: Query result as a DataFrame.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    # Read SQL query
    query = Path(file_path).read_text()

    # Create SQLAlchemy engine
    engine = get_engine(database)

    # Execute query using pandas (works directly with SQLAlchemy engine)
    try:
        df = pd.read_sql(query, engine)
        if df.empty:
            print(f"⚠️ Query returned 0 rows from {database}")
        return df
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

def analysis_process() -> pd.DataFrame:
    """
    Example process function. Modify this to call run_sql_query_from_file
    with your actual SQL file paths and databases.
    """
    sql_file = Path(__file__).parent / "query.sql"  # adjust path
    print(sql_file)
    database = "refined"  # replace with actual database
    df = run_sql_query_from_file(sql_file, database)
    return df
