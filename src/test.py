import argparse
import os

from dotenv import load_dotenv

from src.utils import (create_database, create_table, db_connection,
                       formatting_columns_placeholders, get_data, insert_data)

database_exist = False
load_dotenv(".env")
con, mycursor = db_connection(host=os.getenv("host"), user=os.getenv("user"), password=os.getenv("password"))

#utilizing argparse module to push the arguments dynamically
parser = argparse.ArgumentParser(description="Accessing Database test1 for D2P Project") #creating parser
parser.add_argument('-db','--database', required=True, type=str, help='Name of the database') #required
parser.add_argument('-c', '--csv_file', type=str, help='Path to csv file') #optional
parser.add_argument('-t', '--table_name', type=str, help='table name') #optional
args = parser.parse_args()

if not database_exist:
    create_database(mycursor=mycursor, database=args.database)

#check if the csv_file and table_name is provided for inserting data.
if args.csv_file and args.table_name:
    df = get_data(csv_file=args.csv_file)
    schema, placeholder_str = formatting_columns_placeholders(df=df)
    create_table(mycursor=mycursor, database=args.database, table_name=args.table_name, schema=schema)
    insert_data(con=con, mycursor=mycursor, table_name=args.table_name, df=df)
else:
    print("No CSV file or table name provided. Skipping data insertion.")
