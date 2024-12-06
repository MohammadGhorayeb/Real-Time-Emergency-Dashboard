import os
import sqlite3
from flask import current_app, g


def get_db_connection():
    """
    Establishes a database connection if one doesn't exist for the current application context.
    Returns the database connection object.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # Path to the database file
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Enables name-based access to columns
    return g.db


def close_db(e=None):
    """
    Closes the database connection if it exists in the current application context.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def setup_database():
    """
    Initializes the database by executing the schema SQL script.
    """
    db = get_db_connection()
    # Adjust the path to locate schema.sql outside the app folder
    schema_path = os.path.join(
        current_app.root_path, '..', 'schema.sql')  # Move one level up
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    with open(schema_path, mode='r') as f:
        sql_script = f.read()
        try:
            cursor = db.cursor()
            sql_statements = sql_script.split(';')
            for idx, statement in enumerate(sql_statements):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            print("Database setup completed successfully.")
        except sqlite3.Error as error:
            print(f"SQLite error: {error}")
        finally:
            db.commit()
