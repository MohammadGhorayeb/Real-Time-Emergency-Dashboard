# db.py

import sqlite3
import os
from flask import current_app, g


def get_db_connection():
    """
    Establishes a database connection if one doesn't exist for the current application context.
    Returns the database connection object.
    """
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # Enables name-based access to columns
        print("Connected to database at:", os.path.abspath(
            db_path))  # Print the full path
    return g.db


def setup_database():
    """
    Initializes the database by executing the schema SQL script.
    """
    db = get_db_connection()
    with current_app.open_resource('schema.sql', mode='r') as f:
        sql_script = f.read()
        try:
            cursor = db.cursor()
            # Split the SQL script into individual statements
            sql_statements = sql_script.split(';')
            for idx, statement in enumerate(sql_statements):
                statement = statement.strip()  # Remove leading/trailing whitespace
                if statement:  # Skip empty statements
                    try:
                        cursor.execute(statement)
                    except sqlite3.Error as error:
                        print(f"Error in statement #{idx + 1}: {statement}")
                        print(f"SQLite error: {error}")
                        break  # Exit on the first error
            print("Database setup completed successfully.")
        except sqlite3.Error as error:
            print("Error executing script:", error)
        finally:
            db.commit()


def close_db(e=None):
    """
    Closes the database connection if it exists in the current application context.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()
