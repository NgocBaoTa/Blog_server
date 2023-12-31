import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

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
        authorID INTEGER,
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
        userID INTEGER,
        notiType TEXT,  #reply/ comment/ approve/ review/ decline
        status TEXT,  # read/ unread
        notiContent TEXT,
        createdAt INTEGER,
        FOREIGN KEY(userID) REFERENCES User(userID)
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

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