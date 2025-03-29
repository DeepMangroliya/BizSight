"""March 23rd, 2025 - March 28th, 2025"""

from typing import Optional, Tuple

import mysql.connector
import pandas as pd
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor as Cursor


def create_database(mycursor: Cursor,
             database: str
            ) -> Optional[Error]:
    """_summary_

    Args:
        mycursor (Cursor): mysql cursor to make changed into database
        database (str): the database that is being modified
    
    Returns:
        - None
    
    Raises: 
        -  Error if Database creation fails, otherwise none
    """
    #drop db if already exists and create a new one.
    mycursor.execute(f"DROP DATABASE IF EXISTS {database}")
    mycursor.execute(f"CREATE DATABASE {database}")
    mycursor.execute("SHOW DATABASES")
    dbs = mycursor.fetchall()
    dbs = [db[0] for db in dbs]
    if database in dbs:
        print(f"Database: '{database}' created successfully")
    else:
        print(f"Failed to create Database: '{database}'")
        
        
def db_connection(host: str,
                  user: str,
                  password: str,
                  database: Optional[str] = None
                 ) -> Tuple[MySQLConnection, Cursor]:
    """
    Connects to mysql server.

    Args:
        host (str): MySQL Server host
        user (str): MySQL Server username
        password (str): MySQL Server password
        database (optional[str], Default=None): Database name (Default: None)

    Returns:
        tuple (MySQLConnection [Optional], cursor [Optional]): 
        - Connection object and Cursor obhect if successful, otherwise None

    Raises:
        Connection Error: Connection Unsuccessful
    """
    try:
        #connecting to mysql server
        con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        mycursor = con.cursor()
        print(f"Connected to MySQL {'and Database: ' + database if database else ''} +  Successfully")
        return con, mycursor

    except Error as e:
        print(f"Cannot connect to MySQL Server: {e}")
        

def create_table(mycursor: Cursor, table_name: str, schema: str) -> None:
    """Creates Table

    Args:
        mycursor (Cursor): MySQL cursor. 
        table_name (str): table name
        schema (Tuple): defines the columns of the table and its data types

    Returns:
        - None

    Raises:
        - Error if Table creation fails, otherwise None 

    """
    try:
        sql = f"DROP TABLE IF EXISTS {table_name}"
        mycursor.execute(sql)
        print(f"Old Table '{table_name}' dropped before creation.")

        sql = f"CREATE TABLE {table_name} ({schema})"
        mycursor.execute(sql)
        print(f"Table '{table_name}' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

def get_data(csv_file: str) -> Optional[pd.DataFrame]:
    """
    Reads data from a CSV file using pandas and inserts it into the specified MySQL table.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Dataframe containing the CSV data. [Optional]

    Raises:
        FileNotFoundError: If the file is not found.
    """
    try:
        #read data from csv, extarct columns and values separately
        df = pd.read_csv(csv_file)
        # Insert data into MySQL table using insert_data function
        # Drop 'Unnamed:0' column if it exists, ignoring errors if not present
        df.drop(['Unnamed:0'],axis=1,inplace=True,errors='ignore')
        return df
    except FileNotFoundError:
        print(f"File not found: {csv_file}")

def formatting_columns_placeholders(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Generates SQL schema and placeholders based on DataFrame columns.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing the dataset.

    Returns:
        Tuple[str, str]: SQL schema and value placeholders.
    """
    sql_cols = []
    placeholders = []

    #changing python types to sql types
    for col in df.columns:
        if df[col].dtype == 'int64':
            data_type = 'INT'
        elif df[col].dtype == 'float64':
            data_type = 'FLOAT'
        elif df[col].dtype == 'bool':
            data_type = 'BOOLEAN'
        else:
            data_type = 'VARCHAR(255)'
        sql_cols.append(f"{col} {data_type}")
        placeholders.append("%s")

    #converting the list as strings
    schema = ", ".join(sql_cols)
    placeholder_str = f"({', '.join(placeholders)})"

    return schema, placeholder_str
            

def insert_data(con: MySQLConnection, 
                mycursor: Cursor,
                table_name: str,
                df: pd.DataFrame
                ) -> Optional[int]:
    """
    Inserts data into the specified table for specific columns.

    Args:
        con (MySQLConnection): Connection to the MySQL database.
        mycursor (Cursor): MySQL cursor.
        table_name (str): Name of the table.
        df (pd.DataFrame): Pandas DataFrame containing the data.

    Returns:
        int: Number of rows successfully inserted
       
    Raises:
        Error: If insertion fails, otherwise None
    """
    total=0
    schema, placeholders = formatting_columns_placeholders(df)
    cols = ", ".join(df.columns) #deriving column names in the specified df
    sql_query = f"INSERT INTO {table_name} ({cols}) Values {placeholders}"
    
    for _, row in df.iterrows():
        values = tuple(row) #one row data at a time 
        try:
            mycursor.execute(sql_query, values)
            if mycursor.rowcount == 1: #if the number of row inserted is 1 
                total+=1
            con.commit()
        except Error as e:
            print(e)
    return total
        