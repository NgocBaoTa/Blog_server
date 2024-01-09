from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, userID, username, email, password, userType, avatar, description, createdAt, updatedAt, is_active=True):
        self.userID = userID
        self.username = username
        self.email = email
        self.password = password
        self.userType = userType
        self.avatar = avatar
        self.description = description
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.is_active = is_active

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.userID