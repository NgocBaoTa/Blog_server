from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

comment = Blueprint('comment', __name__)

@comment.route('/<int:postID>', methods=['GET'])
def get_comment_by_post(postID):
    try:
        with get_connection() as connection:
            comment = db.get_comment_by_post(connection, postID)
            return jsonify(comment), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@comment.route('/<int:commentID>', methods=['GET'])
def get_comment_by_id(commentID):
    try:
        with get_connection() as connection:
            comment = db.get_comment_by_id(connection, commentID)
            if comment:
                return jsonify(comment), 200
            else:
                return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
    

@comment.route('/', methods=["POST"])
@login_required
def create_comment():
        try:
            with get_connection() as connection:
                userID = request.json['userID']
                postID = request.json['postID']
                message = request.json['message']
                createdAt = datetime.now()
                updatedAt = datetime.now()
                try:
                    inserted_id = db.add_comment(connection, userID, postID, message, createdAt, updatedAt)
                    return jsonify({"message": "Add comment successfully", "commentID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
        except Exception as e:
            return jsonify(str(e)), 400


@comment.route('/<int:commentID>', methods=['PUT'])
@login_required
def update_comment(commentID):
    try:  
        with get_connection() as connection: 
            comment = db.get_comment_by_id(connection, commentID)
                
            if comment:
                if current_user.userID == comment[1]:
                    message = request.json['message']
                    updatedAt = datetime.now()
                    try: 
                        db.update_comment(connection, message, updatedAt, commentID)
                        return jsonify(db.get_comment_by_id(connection, commentID)), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Unauthorized to update this comment."}), 403  
            else:
                return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@comment.route('/<int:commentID>', methods=['DELETE'])
@login_required
def delete_comment(commentID):
    try:   
        with get_connection() as connection: 
            comment = db.get_comment_by_id(connection, commentID)
            if comment:
                if current_user.userID == comment[1] or current_user.userType == 'admin':
                    try: 
                        numEffectedRow = db.delete_comment_by_id(commentID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Comment deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Unauthorized to delete this comment."}), 403  
            else:
                return jsonify({"message": "Comment not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

