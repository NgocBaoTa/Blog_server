from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

viewer = Blueprint('viewer', __name__)

@viewer.route('/', methods=['GET'])
@login_required
def get_viewers():
    try:
        with get_connection() as connection:
            if current_user.userType == 'admin':
                viewers = db.get_all_viewer(connection)
                return jsonify(viewers), 200
            else:
                return jsonify({"message": "Unauthorized to get all viewers."}), 403  
    except Exception as e:
            return jsonify(str(e)), 400 


@viewer.route('/', methods=["POST"])
def create_viewer():
        try:
            with get_connection() as connection:
                username = request.json['username']
                email = request.json['email']
                createdAt = datetime.now()
                try:
                    inserted_id = db.add_viewer(connection, username, email, createdAt)
                    return jsonify({"message": "Add viewer successfully", "viewerID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
        except Exception as e:
            return jsonify(str(e)), 400
    

@viewer.route('/<int:viewerID>', methods=['DELETE'])
@login_required
def delete_viewer(viewerID):
    if current_user.userType == 'admin':
        try:   
            with get_connection() as connection: 
                viewer = db.get_viewer_by_id(connection, viewerID)
                if viewer:
                    try: 
                        numEffectedRow = db.delete_viewer_by_id(viewerID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Viewer deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Viewer not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to delete this viewer."}), 403  
