from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from server.connection_pool import get_connection

media = Blueprint('media', __name__)

@media.route('/<int:postID>', methods=['GET'])
def get_media_by_post(postID):
    try:
        with get_connection() as connection:
            media = db.get_media_by_post(connection, postID)
            return jsonify(media), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@media.route('/<int:mediaID>', methods=['GET'])
def get_media_by_id(mediaID):
    try:
        with get_connection() as connection:
            media = db.get_media_by_id(connection, mediaID)
            if media:
                return jsonify(media), 200
            else:
                return jsonify({"message": "Media not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
    

@media.route('/', methods=["POST"])
@login_required
def create_media():
        try:
            with get_connection() as connection:
                postID = request.json['postID']
                mediaType = request.json['mediaType']
                mediaUrl = request.json['mediaUrl']
                size = request.json['size']
                try:
                    inserted_id = db.add_media(connection, postID, mediaType, mediaUrl, size)
                    return jsonify({"message": "Add media successfully", "mediaID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
        except Exception as e:
            return jsonify(str(e)), 400


@media.route('/<int:mediaID>', methods=['PUT'])
@login_required
def update_media(mediaID):
    try:  
        with get_connection() as connection: 
            media = db.get_media_by_id(connection, mediaID)
                
            if media:
                if current_user.userID == media[1]:
                    mediaType = request.json['mediaType']
                    mediaUrl = request.json['mediaUrl']
                    size = request.json['size']
                    try: 
                        db.update_media(connection, mediaType, mediaUrl, size, mediaID)
                        return jsonify(db.get_media_by_id(connection, mediaID)), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Unauthorized to update this media."}), 403  
            else:
                return jsonify({"message": "Media not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@media.route('/<int:mediaID>', methods=['DELETE'])
@login_required
def delete_media(mediaID):
    try:   
        with get_connection() as connection: 
            media = db.get_media_by_id(connection, mediaID)
            if media:
                if current_user.userID == media[1] or current_user.userType == 'admin':
                    try: 
                        numEffectedRow = db.delete_media_by_id(mediaID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Media deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Unauthorized to delete this media."}), 403  
            else:
                return jsonify({"message": "Media not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

