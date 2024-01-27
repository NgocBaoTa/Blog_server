from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import server.db as db
from datetime import datetime
from server.connection_pool import get_connection

post = Blueprint('post', __name__)

@post.route('/', methods=['GET'])
def get_posts():
    try:
        with get_connection() as connection:
            posts = db.get_all_post(connection)
            return jsonify(posts), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@post.route('/<int:postID>', methods=['GET'])
def get_post_by_id(postID):
    try:
        with get_connection() as connection:
            post = db.get_post_by_id(connection, postID)
            if post:
                return jsonify(post), 200
            else:
                return jsonify({"message": "Post not found."}), 400
    except Exception as e:
            return jsonify(str(e)), 400 
    

@post.route('/author/<int:authorID>', methods=['GET'])
def get_post_by_author(authorID):
    try:
        with get_connection() as connection:
            posts = db.get_post_by_author(connection, authorID)
            return jsonify(posts), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@post.route('/category/<int:categoryID>', methods=['GET'])
def get_post_by_category(categoryID):
    try:
        with get_connection() as connection:
            posts = db.get_post_by_category(connection, categoryID)
            return jsonify(posts), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@post.route('/latest-posts', methods=['GET'])
def get_latest_post():
    try:
        with get_connection() as connection:
            posts = db.get_latest_post(connection)
            return jsonify(posts), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@post.route('/search', methods=['GET'])
def search_post():
    try:
        with get_connection() as connection:
            search_text = request.args.get('q', '')
            posts = db.search_post(connection, search_text)
            return jsonify(posts), 200
    except Exception as e:
            return jsonify(str(e)), 400 


@post.route('/', methods=["POST"])
@login_required
def create_post():
        try:
            with get_connection() as connection:
                categoryID = request.json['categoryID']
                postTitle = request.json['postTitle']
                postContent = request.json['postContent']
                postType = request.json['postType']
                authorEmail = request.json['authorEmail']
                createdAt = datetime.now()
                updatedAt = datetime.now()
                
                post_author_id = []
                try:
                    inserted_id = db.add_post(connection, categoryID, postTitle, postContent, postType, createdAt, updatedAt)
                    post_author_id.append(db.add_post_author(connection, inserted_id, current_user.userID))
                    if authorEmail:
                        for author in authorEmail:
                            authorID = db.get_user_by_email(connection, author)[0]
                            post_author_id.append(db.add_post_author(connection, inserted_id, authorID))
                    return jsonify({"message": "Add post successfully", "postID": str(inserted_id), "post_author_id": post_author_id}), 200
                except Exception as e:
                    return jsonify({"ERROR": str(e)}), 500
        except Exception as e:
            return jsonify(str(e)), 400


@post.route('/<int:postID>', methods=['PUT'])
@login_required
def update_post(postID):
    try:  
        with get_connection() as connection: 
            post = db.get_post_by_id(connection, postID)
                
            if post:
                authors = db.get_author_by_post(connection, postID)
                isAuthorized = False
                for author in authors:
                    if current_user.userID == author[0]:
                        categoryID = request.json['categoryID']
                        postTitle = request.json['postTitle']
                        postContent = request.json['postContent']
                        postStatus = request.json['postStatus']
                        updatedAt = datetime.now()
                        try: 
                            db.update_post(connection, categoryID, postTitle, postContent, postStatus, updatedAt, postID)
                            isAuthorized = True
                            return jsonify(db.get_post_by_id(connection, postID)), 200
                        except Exception as e:
                            return jsonify(str(e)), 400
                
                if not isAuthorized:
                    return jsonify({"message": "Unauthorized to update this post."}), 403  
            else:
                return jsonify({"message": "Post not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400
    

@post.route('/<int:postID>', methods=['DELETE'])
@login_required
def delete_post(postID):
    try:   
        with get_connection() as connection: 
            post = db.get_post_by_id(connection, postID)
            if post:
                isAuthorized = False
                if current_user.userType == 'admin':
                    isAuthorized = True
                else:
                    authors = db.get_author_by_post(connection, postID)
                    for author in authors:
                        if current_user.userID == author[0]:
                            isAuthorized = True
                            break
                
                if not isAuthorized:
                    return jsonify({"message": "Unauthorized to delete this post."}), 403 
                else:
                    try: 
                        numEffectedRow = db.delete_post_by_id(postID)
                        return jsonify({"NumEffectedRow": numEffectedRow, "message": "Post deleted."}), 200
                    except Exception as e:
                        return jsonify(str(e)), 400
            else:
                return jsonify({"message": "Post not found."}), 400
    except Exception as e:
        return jsonify(str(e)), 400

