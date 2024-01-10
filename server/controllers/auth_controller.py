from flask import Blueprint, request, jsonify
import server.db as db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from dotenv import load_dotenv, find_dotenv
import os                      
from datetime import datetime
from server.connection_pool import get_connection
from server.static.index import convert_to_local_time
from server.model.user_model import User


auth = Blueprint('auth', __name__)

load_dotenv(find_dotenv())
hash_password_string = os.environ.get('HASH_PWD_METHOD')


@auth.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]

    try:
        with get_connection() as connection:
            user = db.get_user_by_email(connection, email)
            if user and check_password_hash(user[3], password):
                createdAt = convert_to_local_time(user[7])
                updatedAt = convert_to_local_time(user[8])
                user_instance = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], createdAt, updatedAt)    # Create the User instance

                print(f"USER_INSTANCE: {user_instance}")
                login_user(user_instance, remember=True)  # Log in the user
                return jsonify({"message": "Login successfully!"}), 200 
            elif user:
                return jsonify({"message": "Incorrect email or password!"}), 400 
            else:
                return jsonify({"message": "User does not exist."}), 400
    except Exception as e:
        return jsonify(str(e)), 400 


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully!"}), 200


@auth.route('/register', methods=['POST'])
def register():
    email = request.json['email']

    try:
        with get_connection() as connection:
            user = db.get_user_by_email(connection, email)

            if user:
                return jsonify({"message": "User already existed."}), 400
            else:
                password = generate_password_hash(request.json['password'], method=hash_password_string)
                username = request.json['username']
                userType = request.json['userType']
                avatar = "https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o="
                description = "Sample description"
                createdAt = datetime.now()
                updatedAt = datetime.now()
                try:
                    inserted_id = db.add_user(connection, username, email, password, userType, avatar, description, createdAt, updatedAt)
                    return jsonify({"message": "Register successfully", "userID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
    except Exception as e:
            return jsonify(str(e)), 400 
