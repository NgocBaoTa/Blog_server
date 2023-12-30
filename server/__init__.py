import os
from flask import Flask, request
import psycopg2
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from bson.objectid import ObjectId

load_dotenv()
database_url = os.getenv("DATABASE_URL")

CREATE_CATEGORY_TABLE = (
    "CREATE TABLE IF NOT EXISTS Category (category_id SERIAL PRIMARY KEY, category_name TEXT);"
)

INSERT_CATEGORY_RETURN_ID = "INSERT INTO Category (category_name) VALUES (%s) RETURNING category_id;"

def create_app():
    app = Flask(__name__)

    connection = psycopg2.connect(database_url)
    
    @app.post("/category")
    def create_category():
        data = request.get_json()
        category_name = data["category_name"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_CATEGORY_TABLE)
                cursor.execute(INSERT_CATEGORY_RETURN_ID, (category_name,))
                category_id = cursor.fetchone()[0]
        return {"category_id": category_id, "message": f"Category {category_name} created."}, 201
    

    @app.route('/')
    def home():
        return "Welcome to the home page!"


    return app
