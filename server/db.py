import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(database_url)

# ============================= CREATE TABLES =============================

CREATE_CATEGORY_TABLE = """
    CREATE TABLE IF NOT EXISTS Category (
        categoryID SERIAL PRIMARY KEY, 
        categoryName TEXT,
        createdAt INTEGER,
        updatedAt INTEGER,
    );
"""

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS User (
        userID SERIAL PRIMARY KEY, 
        username TEXT,
        email TEXT,
        password TEXT,
        userType TEXT,
        avatar TEXT,
        description TEXT,
        createdAt INTEGER,
        updatedAt INTEGER,
    );
"""

CREATE_VIEWER_TABLE = """
    CREATE TABLE IF NOT EXISTS Viewer (
        viewerID SERIAL PRIMARY KEY, 
        username TEXT,
        email TEXT,
        createdAt INTEGER,
        updatedAt INTEGER,
    );
"""

CREATE_POST_TABLE = """
    CREATE TABLE IF NOT EXISTS Post (
        postID SERIAL PRIMARY KEY,
        categoryID INTEGER, 
        authorID INT[],
        postTitle TEXT,
        postContent TEXT,
        postType TEXT,  # posted/ updated/reviewing
        createdAt INTEGER,
        updatedAt INTEGER,
        FOREIGN KEY(authorID) REFERENCES User(userID)
        FOREIGN KEY(categoryID) REFERENCES Category(categoryID)
    );
"""

CREATE_COMMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS Comment (
        commentID SERIAL PRIMARY KEY, 
        userID INTEGER, 
        postID INTEGER,
        message TEXT, 
        replies INT[],  # array of commentID
        createdAt INTEGER,
        updatedAt INTEGER,
        FOREIGN KEY(userID) REFERENCES User(userID)
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

CREATE_MEDIA_TABLE = """
    CREATE TABLE IF NOT EXISTS Media (
        mediaID SERIAL PRIMARY KEY, 
        postID INTEGER,
        mediaType TEXT,
        mediaUrl TEXT,
        size FLOAT[],  # contains 2 elements: width and height
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

CREATE_NOTIFICATION_TABLE = """
    CREATE TABLE IF NOT EXISTS Notification (
        notificationID SERIAL PRIMARY KEY, 
        postID INTEGER,
        userID INT[],  # because 1 post can have multiple authors
        notiType TEXT,  #reply/ comment/ approve/ review/ decline
        status TEXT,  # read/ unread
        notiContent TEXT,
        createdAt INTEGER,
        FOREIGN KEY(userID) REFERENCES User(userID)
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""


# ============================= INSERT DATA ===============================

INSERT_CATEGORY_RETURN_ID = """
    INSERT INTO Category (
        categoryName,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s) 
    RETURNING categoryID;
"""

INSERT_USER_RETURN_ID = """
    INSERT INTO User (
        username,
        email,
        password,
        userType,
        avatar,
        description,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
    RETURNING userID;
"""

INSERT_VIEWER_RETURN_ID = """
    INSERT INTO Viewer (
        username,
        email,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s)  
    RETURNING viewerID;
"""

INSERT_POST_RETURN_ID = """
    INSERT INTO Post (
        categoryID, 
        authorID,
        postTitle,
        postContent,
        postType,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) 
    RETURNING postID;
"""

INSERT_COMMENT_RETURN_ID = """
    INSERT INTO Comment (
        userID, 
        postID,
        message, 
        replies,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING commentID;
"""

INSERT_MEDIA_RETURN_ID = """
    INSERT INTO Media (
        postID,
        mediaType,
        mediaUrl,
        size
    ) VALUES (%s, %s, %s, %s) 
    RETURNING mediaID;
"""

INSERT_NOTIFICATION_RETURN_ID = """
    INSERT INTO Notification (
        postID,
        userID,
        notiType,  
        status,  
        notiContent,
        createdAt
    ) VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING notificationID;
"""


# ============================= GET DATA ===============================

# Get category
GET_ALL_CATEGORY = " SELECT * FROM Category; "
GET_CATEGORY_BY_ID = " SELECT * FROM Category WHERE categoryID = %s; "

# Get comment
GET_COMMENT_BY_ID = " SELECT * FROM Comment WHERE commentID = %s; "
GET_COMMENT_BY_POST = " SELECT * FROM Comment WHERE postID = %s; "

# Get media
GET_MEDIA_BY_ID = " SELECT * FROM Media WHERE mediaID = %s; "
GET_MEDIA_BY_POST = " SELECT * FROM Media WHERE postID = %s; "

# Get notification 
GET_NOTIFICATION_BY_ID = " SELECT * FROM Notification WHERE notificationID = %s; "
GET_NOTIFICATION_BY_USER = " SELECT * FROM Notification WHERE userID = %s; "

# Get post
GET_ALL_POST = " SELECT * FROM Post; "
GET_POST_BY_ID = " SELECT * FROM Post WHERE postID = %s; "
GET_POST_BY_AUTHOR = " SELECT * FROM Post WHERE authorID = %s; "
GET_LATEST_POST = " SELECT * FROM Post  "
SEARCH_POST = "  "

# Get user
GET_ALL_USERS = " SELECT * FROM User; "
GET_USER_BY_ID = " SELECT * FROM User WHERE userID = %s; "

# Get viewer
GET_ALL_VIEWER = " SELECT * FROM Viewer; "

            
# ============================= CREATE TABLES =============================
    
def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CATEGORY_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_VIEWER_TABLE)
            cursor.execute(CREATE_POST_TABLE)
            cursor.execute(CREATE_COMMENT_TABLE)
            cursor.execute(CREATE_MEDIA_TABLE)
            cursor.execute(CREATE_NOTIFICATION_TABLE)


# ============================= INSERT DATA ===============================

def add_category(categoryName, createdAt, updatedAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CATEGORY_RETURN_ID, (categoryName, createdAt, updatedAt))
            return cursor.fetchone()[0]


def add_user(username, email, password, userType, avatar, description, createdAt, updatedAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER_RETURN_ID, (username, email, password, userType, avatar, description, createdAt, updatedAt))
            return cursor.fetchone()[0]


def add_viewer(username, email, createdAt, updatedAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VIEWER_RETURN_ID, (username, email, createdAt, updatedAt))
            return cursor.fetchone()[0]


def add_post(categoryID, authorID, postTitle, postContent, postType, createdAt, updatedAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POST_RETURN_ID, (categoryID, authorID, postTitle, postContent, postType, createdAt, updatedAt))
            return cursor.fetchone()[0]


def add_comment(userID, postID, message, replies, createdAt, updatedAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_COMMENT_RETURN_ID, (userID, postID, message, replies, createdAt, updatedAt))
            return cursor.fetchone()[0]


def add_media(postID, mediaType, mediaUrl, size):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MEDIA_RETURN_ID, (postID, mediaType, mediaUrl, size))
            return cursor.fetchone()[0]


def add_notification(postID, userID, notiType, status, notiContent, createdAt):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_NOTIFICATION_RETURN_ID, (postID, userID, notiType, status, notiContent, createdAt))
            return cursor.fetchone()[0]
            

