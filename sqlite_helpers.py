"""
This file contains helper functions for creating and managing sqlite databases.
Created by Joshua Yalung.
"""
import sqlite3
connection = sqlite3.connect('urls.db') # connect to database (creates if none found)
cursor = connection.cursor()

# this function creates a table in the database
def table_creation():
    # the function creates a table that has:
    # url, alias, timestamp, and id.
    cursor.execute("CREATE TABLE url(link, alias, timestamp, id)")

def table_insert(link, alias, timestamp, id):
    # the function inserts a row into the table
    input = f'INSERT INTO urls VALUES({link}, {alias}, {timestamp}, {id})'
    cursor.execute(input)
    connection.commit()

def table_delete(link):
    # the function deletes a row from the table
    input = f'DELETE FROM urls WHERE link={link}'
    cursor.execute(input)
    connection.commit()

def table_list():
    # the function lists all the rows in the table
    result = cursor.execute("SELECT * FROM urls")
    return result.fetchall()

def table_retrieve(alias):
    # the function retrieves a row from the table
    result = cursor.execute(f'SELECT link, alias, timestamp, id FROM urls WHERE alias={alias}')
    return result.fetchone()