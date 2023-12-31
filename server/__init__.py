from flask import Flask
from flask_login import LoginManager
from server.connection_pool import get_connection
import server.db as db 
from server.model.user_model import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "random" 

    with get_connection() as connection:
        db.create_tables(connection)

    from server.controllers.auth_controller import auth
    from server.controllers.category_controller import category
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(category, url_prefix='/category')

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
