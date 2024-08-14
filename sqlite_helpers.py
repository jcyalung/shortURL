"""
This file contains helper functions for creating and managing sqlite databases.
Created by Joshua Yalung. :)
"""
import sqlite3
from datetime import datetime

LINK_EXAMPLE = ["https://www.youtube.com/watch?v=2yRmwZlv_3s","goofy","apr10",1]
# this function creates a table in the database
def create_table(filename):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function creates a table that has:
    # url, alias, timestamp, and id.
    try:
        cursor.execute("CREATE TABLE urls("
                        "link varchar(255)," 
                        "alias varchar(50)," 
                        "timestamp DATETIME NOT NULL," 
                        "id INTEGER PRIMARY KEY AUTOINCREMENT)")
    except Exception as e:
        print(e)

def insert_url(filename, link, alias):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # if url with alias already exists
    if retrieve_url(filename, alias):
        return False
    # the function inserts a row into the table
    input = f'INSERT INTO urls(link, alias, timestamp) VALUES(?, ?, ?)'
    val = (link, alias, datetime.now())
    cursor.execute(input, val)
    connection.commit()
    return True
    

def delete_url(filename, alias):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function deletes a row from the table
    try:
        input = f'DELETE FROM urls WHERE alias="{alias}"'
        cursor.execute(input)
        connection.commit()
        # check if entries have changed
        if(cursor.rowcount() > 0):
            return True
        else:
            return False
    except Exception as e:
        return False

def list_urls(filename):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function lists all the rows in the table
    result = cursor.execute("SELECT * FROM urls")
    return result.fetchall()

def retrieve_url(filename, alias):
    connection = sqlite3.connect(filename) # connect to database (creates if none found)
    cursor = connection.cursor()
    # the function retrieves a row from the table
    result = cursor.execute(f'SELECT link, alias, timestamp, id FROM urls WHERE alias="{alias}"')
    return result.fetchone()
