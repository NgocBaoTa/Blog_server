from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

notification = Blueprint('notification', __name__)

@notification.route('/<int:userID>', methods=['GET'])
@login_required
def get_notification_by_user(userID):
    try:
        with get_connection() as connection:
            if current_user.userID == userID or current_user.userType == 'admin':
                user = db.get_user_by_id(connection, userID)
                if user:
                    notification = db.get_notification_by_user(connection, userID)
                    return jsonify(notification), 200
                else:
                    return jsonify({"message": "User not found."}), 400
            else:
                return jsonify({"message": "Unauthorized to get this notification."}), 403
    except Exception as e:
            return jsonify(str(e)), 400 


@notification.route('/<int:notificationID>', methods=['GET'])
@login_required
def get_notification_by_id(notificationID):
    try:
        with get_connection() as connection:
            notification = db.get_notification_by_id(connection, notificationID)
            if notification and (current_user.userID == notification[2] or current_user.userType == 'admin'):
                return jsonify(notification), 200
            elif notification and (current_user.userID != notification[2] and current_user.userType != 'admin'):
                return jsonify({"message": "Unauthorized to get this notification."}), 403
            else:
                return jsonify({"message": "Notification not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
    

@notification.route('/', methods=["POST"])
@login_required
def create_notification():
    try:
        with get_connection() as connection:
            if current_user.userType == 'admin':
                postID = request.json['postID']
                userID = request.json['userID']
                notiType = request.json['notiType']
                status = request.json['status']
                notiContent = request.json['notiContent']
                createdAt = datetime.now()
                updatedAt = datetime.now()
                try:
                    inserted_id = db.add_notification(connection, postID, userID, notiType, status, notiContent, createdAt, updatedAt)
                    return jsonify({"message": "Add notification successfully", "notificationID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
            else:
                return jsonify({"message": "Unauthorized to create notification."}), 403
    except Exception as e:
        return jsonify(str(e)), 400


@notification.route('/<int:notificationID>', methods=['PUT'])
@login_required
def update_notification_by_id(notificationID):
    try:  
        with get_connection() as connection: 
            notification = db.get_notification_by_id(connection, notificationID)
                
            if notification and (current_user.userID == notification[2] or current_user.userType == 'admin'):
                status = request.json['status']
                updatedAt = datetime.now()
                try: 
                    db.update_notification_by_id(connection, status, updatedAt, notificationID)
                    return jsonify(db.get_notification_by_id(connection, notificationID)), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            elif notification and current_user.userID != notification[2] and current_user.userType != 'admin':
                return jsonify({"message": "Unauthorized to update this notification."}), 403  
            else:
                return jsonify({"message": "Notification not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@notification.route('/<int:userID>', methods=['PUT'])
@login_required
def update_notification_by_user(userID):
    try:  
        with get_connection() as connection: 
            if current_user.userID == userID or current_user.userType == 'admin':
                status = request.json['status']
                updatedAt = datetime.now()
                try: 
                    db.update_notification_by_user(connection, status, updatedAt, userID)
                    return jsonify(db.get_notification_by_user(connection, userID)), 200
                except Exception as e:
                    return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Unauthorized to update this notification."}), 403  
    except Exception as e:
        return jsonify(str(e)), 400
    

@notification.route('/<int:notificationID>', methods=['DELETE'])
@login_required
def delete_notification(notificationID):
    try:   
        with get_connection() as connection: 
            notification = db.get_notification_by_id(connection, notificationID)
            if notification:
                if current_user.userID == notification[2] or current_user.userType == 'admin':
                    try: 
                        numEffectedRow = db.delete_notification_by_id(notificationID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Notification deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Unauthorized to delete this notification."}), 403  
            else:
                return jsonify({"message": "Notification not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

