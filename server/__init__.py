from flask import Flask
from flask_login import LoginManager
from server.connection_pool import get_connection
import server.db as db 
from server.model.user_model import User
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # CORS(app, origins="http://localhost:4200")
    # CORS(app, origins="http://localhost:4200", supports_credentials=True)
    # CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
    CORS(app)
    app.config['SECRET_KEY'] = "random" 

    with get_connection() as connection:
        db.create_tables(connection)

    from server.controllers.auth_controller import auth
    from server.controllers.category_controller import category
    from server.controllers.comment_controller import comment
    from server.controllers.media_controller import media
    from server.controllers.notification_controller import notification
    from server.controllers.post_controller import post
    from server.controllers.user_controller import user
    from server.controllers.viewer_controller import viewer

    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(category, url_prefix='/category')
    app.register_blueprint(comment, url_prefix='/comment')
    app.register_blueprint(media, url_prefix='/media')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(viewer, url_prefix='/viewer')

    @app.route('/')
    def home():
        return "Welcome to the home page!"

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with get_connection() as connection:
        @login_manager.user_loader
        def load_user(id):
            user_data = db.get_user_by_id(connection, id)
            if user_data:
                user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8])
                return user
            else:
                return None
    

    return app
