from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

user = Blueprint('user', __name__)

@user.route('/', methods=['GET'])
@login_required
def get_users():
    try:
        with get_connection() as connection:
            if current_user.userType == 'admin':
                users = db.get_all_user(connection)
                return jsonify(users), 200
            else:
                return jsonify({"message": "Unauthorized to get all users."}), 403  
    except Exception as e:
            return jsonify(str(e)), 400 


@user.route('/<userID>', methods=['GET'])
def get_user_by_id(userID):
    try:
        with get_connection() as connection:
            user = db.get_user_by_id(connection, userID)
            if user:
                return jsonify(user), 200
            else:
                return jsonify({"message": "User not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 


@user.route('/<postID>', methods=['GET'])
def get_author_by_post(postID):
    try:
        with get_connection() as connection:
            author = db.get_author_by_post(connection, postID)
            if author:
                return jsonify(author), 200
            else:
                return jsonify({"message": "Author not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
        
        
@user.route('/<int:userID>', methods=['PUT'])
@login_required
def update_user(userID):
    if current_user.userID == userID or current_user.userType == 'admin':
        try:  
            with get_connection() as connection: 
                user = db.get_user_by_id(connection, userID)
                if user:
                    username = request.json['username']
                    email = request.json['email']
                    password = request.json['password']
                    userType = request.json['userType']
                    avatar = request.json['avatar']
                    description = request.json['description']
                    updatedAt = datetime.now()
                    try: 
                        db.update_user(connection, username, email, password, userType, avatar, description, updatedAt, userID)
                        return jsonify(db.get_user_by_id(connection, userID)), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "User not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to update this user."}), 403  
    

@user.route('/<int:userID>', methods=['DELETE'])
@login_required
def delete_user(userID):
    if current_user.userID == userID or current_user.userType == 'admin':
        try:   
            with get_connection() as connection: 
                user = db.get_user_by_id(connection, userID)
                if user:
                    try: 
                        numEffectedRow = db.delete_user_by_id(userID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "User deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "User not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to delete this user."}), 403  
