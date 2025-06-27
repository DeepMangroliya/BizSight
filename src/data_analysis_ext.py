import os
from typing import Optional
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine

# Load environment variables from the .env file in the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

def run_sql_query_from_file(file_path: Path, database: str) -> Optional[pd.DataFrame]:
    """
    Executes a SQL query from a .sql file using SQLAlchemy engine and returns the result as a DataFrame.

    Args:
        file_path : Path
            Path to the SQL file.
        database : str
            Name of the database to connect to.

    Returns: 
        Optional[pd.DataFrame] : 
            Query result as a DataFrame if successful, else None.
    """
    user = os.getenv('USER') or 'root'
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')

    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    try:
        with open(file_path, 'r') as f:
            query = f.read()

        df = pd.read_sql(query, engine)
        print(f"✅ Query executed successfully. {len(df)} rows retrieved.")
        return df

    except FileNotFoundError:
        print(f"❌ Query file not found: {file_path}")
    except Exception as e:
        print(f"❌ Error executing query from file: {e}")

    return None

def process() -> None:
    """
    Runs a SQL query from file, loads data, and returns the DataFrame.

    Returns:
        None
    """
    file_path = PROJECT_ROOT / "src" / "query.sql"
    database = "refined"  # Ensure this matches your actual DB name

    data = run_sql_query_from_file(file_path=file_path, database=database)
    return data

if __name__ == "__main__":
    process()
