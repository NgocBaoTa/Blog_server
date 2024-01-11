from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

category = Blueprint('category', __name__)

@category.route('/', methods=['GET'])
def get_categories():
    try:
        with get_connection() as connection:
            categories = db.get_all_category(connection)
            return jsonify(categories), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@category.route('/<categoryID>', methods=['GET'])
def get_category_by_id(categoryID):
    try:
        with get_connection() as connection:
            category = db.get_category_by_id(connection, categoryID)
            if category:
                return jsonify(category), 200
            else:
                return jsonify({"message": "Category not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
        

@category.route('/', methods=["POST"])
@login_required
def create_category():
    if current_user.userType == "admin":
        try:
            with get_connection() as connection:
                categoryName = request.json['categoryName']
                createdAt = datetime.now()
                updatedAt = datetime.now()
                try:
                    inserted_id = db.add_category(connection, categoryName, createdAt, updatedAt)
                    return jsonify({"message": "Add category successfully", "categoryID": str(inserted_id)}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
        except Exception as e:
            return jsonify(str(e)), 400 
    else:
        return jsonify({"message": "Unauthorized to create category."}), 403  



@category.route('/<int:categoryID>', methods=['PUT'])
@login_required
def update_category(categoryID):
    if current_user.userType == 'admin':
        try:  
            with get_connection() as connection: 
                category = db.get_category_by_id(connection, categoryID)
                if category:
                    categoryName = request.json['categoryName']
                    updatedAt = datetime.now()
                    try: 
                        db.update_category(connection, categoryName, updatedAt, categoryID)
                        return jsonify(db.get_category_by_id(connection, categoryID)), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Category not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to update this category."}), 403  
    

@category.route('/<int:categoryID>', methods=['DELETE'])
@login_required
def delete_category(categoryID):
    if current_user.userType == 'admin':
        try:   
            with get_connection() as connection: 
                category = db.get_category_by_id(connection, categoryID)
                if category:
                    try: 
                        numEffectedRow = db.delete_category_by_id(categoryID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Category deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
                else:
                    return jsonify({"message": "Category not found."}), 400
        except Exception as e:
            return jsonify(str(e)), 400
    else:
        return jsonify({"message": "Unauthorized to delete this category."}), 403  
