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


