import os
from flask import Flask
from db import setup_database, close_db  # Import from the parent directory


def create_app():
    app = Flask(__name__)
    # Path to your SQLite database file
    app.config['DATABASE'] = os.path.join(app.instance_path, 'app.db')

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Register database teardown function
    app.teardown_appcontext(close_db)

    # Setup the database schema
    with app.app_context():
        setup_database()

    return app
