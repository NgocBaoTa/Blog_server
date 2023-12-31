import os
from flask import Flask, request
from connection_pool import get_connection
import db

def create_app():
    app = Flask(__name__)

    with get_connection() as connection:
        db.create_tables(connection)
    

    @app.route('/')
    def home():
        return "Welcome to the home page!"


    return app
