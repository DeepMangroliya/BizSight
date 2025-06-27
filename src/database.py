import argparse
import os
import yaml
from pathlib import Path

from dotenv import load_dotenv

from utils import (create_database, create_table, db_connection,
                   formatting_columns_placeholders, get_data, insert_data)

# ──────────────────────────────────────────────
# Parse CLI arguments
parser = argparse.ArgumentParser(description="Accessing Database for D2P Project")
parser.add_argument('-dbn', '--database_new', default=False, type=bool,
                    help='Use existing database or create a new database')
parser.add_argument('-db', '--database_name', required=True,
                    type=str, help='Name of the database')
parser.add_argument('-t', '--task_name', type=str,
                    help='task defined in the config file')
args = parser.parse_args()

# ──────────────────────────────────────────────
# Setup project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables safely regardless of working directory
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Load config YAML safely using full path
with open(PROJECT_ROOT / "config" / "config.yaml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Connect to MySQL using credentials from .env
con, mycursor = db_connection(
    host=os.getenv("HOST"),
    user="root",
    password=os.getenv("PASSWORD")
)

# ──────────────────────────────────────────────
# Run logic based on arguments
if args.database_new:
    create_database(mycursor=mycursor, database=args.database_name)
else:
    config_import = config[args.task_name]['import']
    for item in config_import:
        # Fix 1: Construct absolute path to CSV file
        data_path = PROJECT_ROOT / item["import"]["dirpath"] / (
            item["import"]["prefix_filename"] + '.' + item["import"]["file_extension"]
        )

        table_name = data_path.stem  # cleaner than os.path.basename
        df = get_data(csv_file=data_path)

        # Fix 2: Add check in case file was missing
        if df is None:
            raise FileNotFoundError(f"ETL stopped: Could not find {data_path}")

        schema, placeholder_str = formatting_columns_placeholders(df=df)
        create_table(mycursor=mycursor, database=args.database_name,
                     table_name=table_name, schema=schema)
        insert_data(con=con, mycursor=mycursor, table_name=table_name, df=df)
