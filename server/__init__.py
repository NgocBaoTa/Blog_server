import os
from flask import Flask, request

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
