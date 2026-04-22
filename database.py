# database.py — handles the connection to our PostgreSQL database

import psycopg2  
# psycopg2 is the library that lets Python communicate with PostgreSQL

def get_connection():
    # this function creates a new connection to the database every time it's called
    conn = psycopg2.connect(
        host="localhost",        # the server where our database lives
        database="inventory_db", # the name of our database
        user="postgres",         # the username to access the database
        password="your_password" # the password — Sedra will give you this
    )
    return conn  
    # we return the connection so other files can use it