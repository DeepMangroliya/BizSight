"""March 23rd, 2025: Starting with Utils file
    created funcitons: -
    1. db_connection
    2. create_table
    3. insert_data
    4. insert_csv_data
    
    - Formulated Doc Strings: -
        1. Must have: -
            a. Summary
            b. Args
            c. Returns
            d. Raises
    
    - try except block for error handling
    
    TO TEST: Import functions in another file.
    
    # TO DO
        [Done] 1. Rewirte all the functions
        [Done] 2. CSV to DB
        [Done] 3. Funcitons needed :-
            [Done, combined with Connect funtion] a. create database [check if db exists or not]
            [Done] b. connect_to_mysqlserver
            [Done] c. creating table [check if db exists or not]
            [Done] d. create the schema for the table, and return table schema, and values placeholder, insert data
        4. Tests the file, import the functions to test it out

"""

from typing import Optional, Tuple

import mysql.connector
from mysql.connector import Error, MySQLConnection

import pandas as pd

def db_connection(host: str, user: str, password: str, database: Optional[str] = None) -> Tuple[Optional[MySQLConnection], Optional[Error]]:
    """
    Connects to mysql server.

    Args:
        host (str): MySQL Server host
        user (str): MySQL Server username
        password (str): MySQL Server password
        database (optional[str], Default=None): Database name (Default: None)

    Returns:
        tuple (MySQLConnection): 
        - Connection object if successful, otherwise None
        - Error Object if fails, otherwise None

    Raises:
        Connection Error: Connection Unsuccessful
    """
    try:
        #connect to server (without specifying the database)
        con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )

        #create database if name is provided, and not exists already
        if database:
            mycursor = con.cursor()
            sql_query = f"CREATE DATABASE IF NOT EXISTS {database}"
            mycursor.execute(sql_query)
            con.commit()
            mycursor.close()
            con.close()

            #reconnect with selected database
            con = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        print(f"Connected to MySQL {'and Database: ' + database if database else ''} +  Successfully")
        return con, None

    except Error as e:
        print(f"Cannot connect to MySQL Server: {e}")
        return None, e


def create_table(con: MySQLConnection, table_name: str, schema: str, replace: bool = False) -> Optional[Error]:
    """Creates Table

    Args:
        con (MySQLConnection): Connection to MySQL database 
        table_name (str): table name
        schema (Tuple): defines the columns of the table and its data types

    Returns:
        - Error Object if fails, otherise None

    Raises:
        - Error if Table creation fails, otherwise None 

    """
    try:
        mycursor = con.cursor()
        if replace:
            sql = f"DROP TABLE IF EXISTS {table_name}"
            mycursor.execute(sql)
            print(f"Old Table '{table_name}' dropped before creation.")

        sql = f"CREATE TABLE {table_name} ({schema})"
        mycursor.execute(sql)
        con.commit()
        mycursor.close()
        print(f"Table '{table_name}' created successfully.")
        return None
    except Error as e:
        print(f"Connot create Table: {e}")
        return e


def insert_data(con: MySQLConnection, table_name: str, columns: list, values: list) -> Optional[Error]:
    """
    Inserts data into the specified table for specific columns.

    Args:
        con (MySQLConnection): Connection to the MySQL database.
        table_name (str): Name of the table to insert data into.
        columns (list): List of columns to insert data into.
        data (list): List of tuples, where each tuple represents a row of data to be inserted.

    Returns:
        Error Object if insertion fails, otherwise None.

    Raises:
        Error if Data Insertion fails, otherwise None.
    """

    try:
        mycursor = con.cursor()
        placeholders = ", ".join(["%s"] * len(values)) #placeholder string for intertion
        columns_names = ", ".join(columns) #columns as string for insertion
        values = ", ".join(values) #values as string for insertion
        sql = f"INSERT INTO {table_name} ({columns_names}) VALUES ({placeholders})"
        mycursor.executemany(sql, values)
        con.commit()
        mycursor.close()
        print(f"Data has been successfully inserted in {table_name}")
        return None
    except Error as e:
        print(f"Cannot insert data into table '{table_name}': {e}")
        return e

def insert_csv_data(con: MySQLConnection, table_name: str, csv_file: str) -> Optional[Error]:
    """
    Reads data from a CSV file using pandas and inserts it into the specified MySQL table.

    Args:
        con (MySQLConnection): Connection to the MySQL database.
        table_name (str): Name of the table to insert data into.
        csv_file (str): Path to the CSV file.

    Returns:
        Error Object if insertion fails, otherwise None.

    Raises:
        Error if CSV reading or Data Insertion fails, otherwise None.
    """
    try:
        #read data from csv, extarct columns and values separately
        df = pd.read_csv(csv_file)
        columns = df.columns.tolist() #getting columns
        values = df.values.tolist() #getting values as list of lists
        
        # Insert data into MySQL table using insert_data function
        return insert_data(con, table_name, columns, values)
    except FileNotFoundError as e:
        print(f"File not found: {csv_file}")
        return e
    except Error as e:
        print(f"Error reading CSV or inserting data: {e}")
        return e

