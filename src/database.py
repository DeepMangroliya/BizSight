import argparse
import os
import yaml
from pathlib import Path

from dotenv import load_dotenv

from utils import (create_database, create_table, db_connection,
                   formatting_columns_placeholders, get_data, insert_data)

# utilizing argparse module to push the arguments dynamically
parser = argparse.ArgumentParser(
    description="Accessing Database test1 for D2P Project")  # creating parser
parser.add_argument('-dbn', '--database_new', default=False, type=bool,
                    help='Use existing database or create a new database')  # optional
parser.add_argument('-db', '--database_name', required=True,
                    type=str, help='Name of the database')  # required
# parser.add_argument('-c', '--csv_file', type=str, help='Path to csv file') #optional
parser.add_argument('-t', '--task_name', type=str,
                    help='task defined in the config file')  # optional
args = parser.parse_args()

# load credentials
load_dotenv(".env")

# load config file
with open("./config/config.yaml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# connect to mysql server
con, mycursor = db_connection(host=os.getenv("HOST"),
                              user="root",
                              password=os.getenv("PASSWORD"))

# check if we are creating a new database or not to create table and insert data accoirdingly.
if args.database_new:
    create_database(mycursor=mycursor, database=args.database_name)
else:
    config_import = config[args.task_name]['import']
    for i in range(len(config_import)):
        data = Path(config_import[i]["import"]["dirpath"],
                    config_import[i]["import"]["prefix_filename"] + '.' +
                    config_import[i]["import"]["file_extension"])
        table_name = os.path.basename(data).split('.')[0]
        df = get_data(csv_file=data)
        schema, placeholder_str = formatting_columns_placeholders(df=df)
        create_table(mycursor=mycursor, database=args.database_name,
                     table_name=table_name, schema=schema)
        insert_data(con=con, mycursor=mycursor, table_name=table_name, df=df)
