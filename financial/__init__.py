import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from financial.model import db


def create_app():
    app = Flask(__name__)

    # Load the environment variables from the .env file.
    load_dotenv()

    # setting for database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]

    return app


app = create_app()
db.init_app(app)
migrate = Migrate(app, db)

# Import the routes after the app is created.
# Circular imports won't happen because we are not using it.
import financial.routes
