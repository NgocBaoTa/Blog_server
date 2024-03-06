from contextlib import contextmanager
from server.static.index import convert_to_utc_time

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

# ============================= CREATE TABLES =============================

CREATE_CATEGORY_TABLE = """
    CREATE TABLE IF NOT EXISTS Category (
        categoryID SERIAL PRIMARY KEY, 
        categoryName TEXT,
        categoryImage TEXT,
        createdAt INTEGER,
        updatedAt INTEGER
    );
"""

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS "User" (
        userID SERIAL PRIMARY KEY, 
        username TEXT,
        email TEXT,
        password TEXT,
        userType TEXT,
        avatar TEXT,
        description TEXT,
        createdAt INTEGER,
        updatedAt INTEGER
    );
"""

CREATE_VIEWER_TABLE = """
    CREATE TABLE IF NOT EXISTS Viewer (
        viewerID SERIAL PRIMARY KEY, 
        username TEXT,
        email TEXT,
        createdAt INTEGER
    );
"""

CREATE_POST_TABLE = """
    CREATE TABLE IF NOT EXISTS Post (
        postID SERIAL PRIMARY KEY,
        categoryID INTEGER, 
        postTitle TEXT,
        postContent TEXT,
        postStatus TEXT,  
        createdAt INTEGER,
        updatedAt INTEGER,
        FOREIGN KEY(categoryID) REFERENCES Category(categoryID)
    );
"""

CREATE_POST_AUTHOR_TABLE = """
    CREATE TABLE IF NOT EXISTS PostAuthor (
        postAuthorID SERIAL PRIMARY KEY,
        postID INTEGER,
        userID INTEGER,
        FOREIGN KEY(userID) REFERENCES "User"(userID),
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

CREATE_COMMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS Comment (
        commentID SERIAL PRIMARY KEY, 
        userID INTEGER, 
        postID INTEGER,
        message TEXT,   
        createdAt INTEGER,
        updatedAt INTEGER,
        FOREIGN KEY(userID) REFERENCES "User"(userID),
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

CREATE_REPLYTO_TABLE = """
    CREATE TABLE IF NOT EXISTS ReplyTo (
        replyToID SERIAL PRIMARY KEY,
        commentID INTEGER,
        responseID INTEGER,
        FOREIGN KEY(commentID) REFERENCES Comment(commentID),
        FOREIGN KEY(responseID) REFERENCES Comment(commentID)
    );
"""

CREATE_MEDIA_TABLE = """
    CREATE TABLE IF NOT EXISTS Media (
        mediaID SERIAL PRIMARY KEY, 
        postID INTEGER,
        mediaType TEXT,
        mediaUrl TEXT,
        size FLOAT[],  
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""

CREATE_NOTIFICATION_TABLE = """
    CREATE TABLE IF NOT EXISTS Notification (
        notificationID SERIAL PRIMARY KEY, 
        postID INTEGER,
        userID INTEGER,  
        notiType TEXT,  
        status TEXT,  
        notiContent TEXT,
        createdAt INTEGER,
        updatedAt INTEGER,
        FOREIGN KEY(userID) REFERENCES "User"(userID),
        FOREIGN KEY(postID) REFERENCES Post(postID)
    );
"""


# ============================= INSERT DATA ===============================

INSERT_CATEGORY_RETURN_ID = """
    INSERT INTO Category (
        categoryName,
        categoryImage,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s) 
    RETURNING categoryID;
"""

INSERT_USER_RETURN_ID = """
    INSERT INTO "User" (
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
        createdAt
    ) VALUES (%s, %s, %s, %s)  
    RETURNING viewerID;
"""

INSERT_POST_RETURN_ID = """
    INSERT INTO Post (
        categoryID, 
        postTitle,
        postContent,
        postStatus,
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING postID;
"""

INSERT_POST_AUTHOR_RETURN_ID = """
    INSERT INTO PostAuthor (
        postID, 
        userID
    ) VALUES (%s, %s) 
    RETURNING postAuthorID;
"""

INSERT_COMMENT_RETURN_ID = """
    INSERT INTO Comment (
        userID, 
        postID,
        message, 
        createdAt,
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s) 
    RETURNING commentID;
"""

INSERT_REPLYTO_RETURN_ID = """
    INSERT INTO ReplyTo (
        commentID,
        responseID
    ) VALUES (%s, %s) 
    RETURNING replyToID;
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
        createdAt, 
        updatedAt
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) 
    RETURNING notificationID;
"""


# ============================= GET DATA ===============================

# Get category
GET_ALL_CATEGORY = " SELECT * FROM Category; "
GET_CATEGORY_BY_ID = " SELECT * FROM Category WHERE categoryID = %s; "
GET_ALL_CATEGORY_WITH_POST = """ 
    SELECT 
        c.categoryID,
        c.categoryName,
        c.categoryImage,
        p.postID,
        p.postTitle,
        p.postContent,
        u.username
    FROM Category c 
    LEFT JOIN Post p 
        ON c.categoryID = p.categoryID 
    LEFT JOIN PostAuthor pa
        ON p.postID = pa.postID
    LEFT JOIN "User" u
        ON pa.userID = u.userID; 
"""

# Get comment
GET_COMMENT_BY_ID = " SELECT * FROM Comment WHERE commentID = %s; "
GET_COMMENT_BY_POST = """
    SELECT *
    FROM Comment c 
        LEFT OUTER JOIN Comment r ON c.commentID = r.commentID  
        LEFT OUTER JOIN ReplyTo rt ON rt.responseID = r.commentID
    WHERE c.postID = %s;
"""

# Get media
GET_MEDIA_BY_ID = " SELECT * FROM Media WHERE mediaID = %s; "
GET_MEDIA_BY_POST = " SELECT * FROM Media WHERE postID = %s; "

# Get notification 
GET_NOTIFICATION_BY_ID = " SELECT * FROM Notification WHERE notificationID = %s; "
GET_NOTIFICATION_BY_USER = " SELECT * FROM Notification WHERE userID = %s; "

# Get post
GET_ALL_POST = """ 
    SELECT p.*, u.* 
    FROM Post p
        JOIN PostAuthor pa ON p.postID = pa.postID
        JOIN "User" u ON u.userID = pa.userID; 
"""

GET_POST_BY_ID = " SELECT * FROM Post WHERE postID = %s; "

GET_POST_BY_AUTHOR = """ 
    SELECT p.*
    FROM Post p
        JOIN PostAuthor pa ON p.postID = pa.postID
    WHERE pa.userID = %s; 
"""

GET_POST_BY_CATEGORY = """ 
    SELECT p.*
    FROM Post p
        JOIN Category c ON p.categoryID = c.categoryID
    WHERE c.categoryID = %s; 
"""

GET_LATEST_POST = " SELECT * FROM Post ORDER BY createdAt DESC LIMIT 10;  "  # get 10 latest created posts

SEARCH_POST = """ 
    SELECT p.*, u.*
    FROM Post p
        JOIN PostAuthor pa ON p.postID = pa.postID
        JOIN "User" u ON u.userID = pa.userID
    WHERE postTitle LIKE %s; 
"""

# Get user
GET_ALL_USER = """ SELECT * FROM "User"; """
GET_USER_BY_ID = """ SELECT * FROM "User" WHERE userID = %s; """
GET_USER_BY_EMAIL = """ SELECT * FROM "User" WHERE email = %s; """

GET_AUTHOR_BY_POST = """ 
    SELECT u.*
    FROM "User" u
        JOIN PostAuthor pa ON a.userID = pa.userID
    WHERE pa.postID = %s; 
"""

# Get viewer
GET_ALL_VIEWER = " SELECT * FROM Viewer; "
GET_VIEWER_BY_ID = """ SELECT * FROM Viewer WHERE viewerID = %s; """


# ============================= UPDATE DATA ===============================

# Update category
UPDATE_CATEGORY_BY_ID = """ 
    UPDATE Category
    SET 
        categoryName = %s, 
        categoryImage = %s,
        updatedAt = %s
    WHERE categoryID = %s;
"""

# Update comment
UPDATE_COMMENT_BY_ID = """ 
    UPDATE Comment
    SET 
        message = %s, 
        updatedAt = %s
    WHERE commentID = %s;
"""

# Update media
UPDATE_MEDIA_BY_ID = """ 
    UPDATE Media
    SET 
        mediaType = %s,
        mediaUrl = %s,
        size = %s
    WHERE mediaID = %s;
"""

# Update notification 
UPDATE_NOTIFICATION_BY_ID = """ 
    UPDATE Notification
    SET 
        status = %s,
        updatedAt = %s
    WHERE notificationID = %s;
"""

UPDATE_NOTIFICATION_BY_USER = """ 
    UPDATE Notification
    SET 
        status = %s,
        updatedAt = %s
    WHERE userID = %s;
"""

# Update post
UPDATE_POST_BY_ID = """ 
    UPDATE Post
    SET 
        categoryID = %s, 
        postTitle = %s,
        postContent = %s,
        postStatus = %s,
        updatedAt = %s
    WHERE postID = %s;
"""

# Update user
UPDATE_USER_BY_ID = """ 
    UPDATE "User"
    SET 
        username = %s,
        email = %s,
        password = %s,
        userType = %s,
        avatar = %s,
        description = %s,
        updatedAt = %s
    WHERE userID = %s;
"""


# ============================= DELETE DATA ===============================

# Delete category
DELETE_CATEGORY_BY_ID = " DELETE FROM Category WHERE categoryID = %s; "

# Delete comment
DELETE_COMMENT_BY_ID = " DELETE FROM Comment WHERE commentID = %s; "
DELETE_COMMENT_BY_POST = " DELETE FROM Comment WHERE postID = %s; "       # CHECK IF WE NEED IT OR AFTER DELETING THE POST, IT WILL AUTOMATICALLY DELETE ALL THE COMMENTS? 

# Delete media
DELETE_MEDIA_BY_ID = " DELETE FROM Media WHERE mediaID = %s; "
DELETE_MEDIA_BY_POST = " DELETE FROM Media WHERE postID = %s; "   # CHECK IF WE NEED IT???

# Delete notification 
DELETE_NOTIFICATION_BY_ID = " DELETE FROM Notification WHERE notificationID = %s; "
DELETE_NOTIFICATION_BY_USER = " DELETE FROM Notification WHERE userID = %s; "

# Delete post
DELETE_POST_BY_ID = " DELETE FROM Post WHERE postID = %s; "

# Delete post_author
DELETE_POST_AUTHOR_BY_ID = " DELETE FROM PostAuthor WHERE postAuthorID = %s; "

# Delete user
DELETE_USER_BY_ID = """ DELETE FROM "User" WHERE userID = %s; """

# Delete viewer
DELETE_VIEWER_BY_ID = " DELETE FROM Viewer WHERE viewerID = %s; "

            

# ============================= CREATE TABLES FUNCTION =============================
    
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_CATEGORY_TABLE)
        cursor.execute(CREATE_USER_TABLE)
        cursor.execute(CREATE_VIEWER_TABLE)
        cursor.execute(CREATE_POST_TABLE)
        cursor.execute(CREATE_POST_AUTHOR_TABLE)
        cursor.execute(CREATE_COMMENT_TABLE)
        cursor.execute(CREATE_REPLYTO_TABLE)
        cursor.execute(CREATE_MEDIA_TABLE)
        cursor.execute(CREATE_NOTIFICATION_TABLE)


# ============================= GET DATA FUNCTIONS ===============================

# Get category
def get_all_category(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_ALL_CATEGORY)
        return cursor.fetchall()

def get_category_by_id(connection, categoryID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_CATEGORY_BY_ID, (categoryID,))
        return cursor.fetchone()

def get_all_category_with_post(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_ALL_CATEGORY_WITH_POST)
        return cursor.fetchall()

# Get user
def get_all_user(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_ALL_USER)
        return cursor.fetchall()

def get_user_by_id(connection, userID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_USER_BY_ID, (userID,))
        return cursor.fetchone()

def get_user_by_email(connection, email):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_USER_BY_EMAIL, (email,))
        return cursor.fetchone()

def get_author_by_post(connection, postID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_AUTHOR_BY_POST, (postID,))
        return cursor.fetchall()

# Get viewer
def get_all_viewer(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_ALL_VIEWER)
        return cursor.fetchall()

def get_viewer_by_id(connection, viewerID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_VIEWER_BY_ID, (viewerID,))
        return cursor.fetchone()

# Get post
def get_all_post(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_ALL_POST)
        return cursor.fetchall()

def get_post_by_id(connection, postID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_POST_BY_ID, (postID,))
        return cursor.fetchone()
    
def get_post_by_author(connection, authorID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_POST_BY_AUTHOR, (authorID,))
        return cursor.fetchall()

def get_post_by_category(connection, categoryID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_POST_BY_CATEGORY, (categoryID,))
        return cursor.fetchall()

def get_latest_post(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_LATEST_POST)
        return cursor.fetchall()

def search_post(connection, search_text):
    with get_cursor(connection) as cursor:
        cursor.execute(SEARCH_POST, (search_text,))
        return cursor.fetchall()

# Get comment
def get_comment_by_id(connection, commentID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_COMMENT_BY_ID, (commentID,))
        return cursor.fetchone()
    
def get_comment_by_post(connection, postID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_COMMENT_BY_POST, (postID,))
        return cursor.fetchall()

# Get media
def get_media_by_id(connection, mediaID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_MEDIA_BY_ID, (mediaID,))
        return cursor.fetchone()
    
def get_media_by_post(connection, postID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_MEDIA_BY_POST, (postID,))
        return cursor.fetchall()

# Get notification
def get_notification_by_id(connection, notificationID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_NOTIFICATION_BY_ID, (notificationID,))
        return cursor.fetchone()
    
def get_notification_by_user(connection, userID):
    with get_cursor(connection) as cursor:
        cursor.execute(GET_NOTIFICATION_BY_USER, (userID,))
        return cursor.fetchall()


# ============================= INSERT DATA FUNCTIONS ===============================

def add_category(connection, categoryName, categoryImage, createdAt, updatedAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        updatedAt = convert_to_utc_time()
        cursor.execute(INSERT_CATEGORY_RETURN_ID, (categoryName, categoryImage, createdAt, updatedAt))
        return cursor.fetchone()[0]


def add_user(connection, username, email, password, userType, avatar, description, createdAt, updatedAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        updatedAt = convert_to_utc_time()
        cursor.execute(INSERT_USER_RETURN_ID, (username, email, password, userType, avatar, description, createdAt, updatedAt))
        return cursor.fetchone()[0]


def add_viewer(connection, username, email, createdAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        cursor.execute(INSERT_VIEWER_RETURN_ID, (username, email, createdAt))
        return cursor.fetchone()[0]


def add_post(connection, categoryID, postTitle, postContent, postType, createdAt, updatedAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        updatedAt = convert_to_utc_time()
        cursor.execute(INSERT_POST_RETURN_ID, (categoryID, postTitle, postContent, postType, createdAt, updatedAt))
        return cursor.fetchone()[0]


def add_post_author(connection, postID, userID):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POST_AUTHOR_RETURN_ID, (postID, userID))
        return cursor.fetchone()[0]


def add_comment(connection, userID, postID, message, createdAt, updatedAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        updatedAt = convert_to_utc_time()
        cursor.execute(INSERT_COMMENT_RETURN_ID, (userID, postID, message, createdAt, updatedAt))
        return cursor.fetchone()[0]


def add_replyto(connection, commentID, responseID):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_REPLYTO_RETURN_ID, (commentID, responseID))
        return cursor.fetchone()[0]


def add_media(connection, postID, mediaType, mediaUrl, size):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_MEDIA_RETURN_ID, (postID, mediaType, mediaUrl, size))
        return cursor.fetchone()[0]


def add_notification(connection, postID, userID, notiType, status, notiContent, createdAt, updatedAt):
    with get_cursor(connection) as cursor:
        createdAt = convert_to_utc_time()
        updatedAt = convert_to_utc_time()
        cursor.execute(INSERT_NOTIFICATION_RETURN_ID, (postID, userID, notiType, status, notiContent, createdAt, updatedAt))
        return cursor.fetchone()[0]


# ============================= UPDATE DATA FUNCTIONS ===============================

def update_category(connection, categoryName, categoryImage, updatedAt, categoryID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_CATEGORY_BY_ID, (categoryName, categoryImage, updatedAt, categoryID))
        return cursor.rowcount()


def update_user(connection, username, email, password, userType, avatar, description, updatedAt, userID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_USER_BY_ID, (username, email, password, userType, avatar, description, updatedAt, userID))
        return cursor.rowcount()


def update_post(connection, categoryID, postTitle, postContent, postStatus, updatedAt, postID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_POST_BY_ID, (categoryID, postTitle, postContent, postStatus, updatedAt, postID))
        return cursor.rowcount()


def update_comment(connection, message, updatedAt, commentID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_COMMENT_BY_ID, (message, updatedAt, commentID))
        return cursor.rowcount()


def update_media(connection, mediaType, mediaUrl, size, mediaID):
    with get_cursor(connection) as cursor:
        cursor.execute(UPDATE_MEDIA_BY_ID, (mediaType, mediaUrl, size, mediaID))
        return cursor.rowcount()


def update_notification_by_id(connection, status, updatedAt, notificationID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_NOTIFICATION_BY_ID, (status, updatedAt, notificationID))
        return cursor.rowcount()


def update_notification_by_user(connection, status, updatedAt, userID):
    with get_cursor(connection) as cursor:
        updatedAt = convert_to_utc_time()
        cursor.execute(UPDATE_NOTIFICATION_BY_USER, (status, updatedAt, userID))
        return cursor.rowcount()


# ============================= DELETE DATA FUNCTIONS ===============================

# Delete category
def delete_category_by_id(connection, categoryID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_CATEGORY_BY_ID, (categoryID,))
        return cursor.rowcount()

# Delete user
def delete_user_by_id(connection, userID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_USER_BY_ID, (userID,))
        return cursor.rowcount()

# Delete viewer
def delete_viewer_by_id(connection, viewerID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_VIEWER_BY_ID, (viewerID,))
        return cursor.rowcount()

# Delete post
def delete_post_by_id(connection, postID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_POST_BY_ID, (postID,))
        return cursor.rowcount()
    
# Delete post_author
def delete_post_author_by_id(connection, postAuthorID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_POST_AUTHOR_BY_ID, (postAuthorID,))
        return cursor.rowcount()
    
# Delete comment
def delete_comment_by_id(connection, commentID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_COMMENT_BY_ID, (commentID,))
        return cursor.rowcount()
      
def delete_comment_by_post(connection, postID):                     # CHECK IF WE NEED IT OR AFTER DELETING THE POST, IT WILL AUTOMATICALLY DELETE ALL THE COMMENTS?              
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_COMMENT_BY_POST, (postID,))
        return cursor.rowcount()

# Delete media
def delete_media_by_id(connection, mediaID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_MEDIA_BY_ID, (mediaID,))
        return cursor.rowcount()
    
def delete_media_by_post(connection, postID):              # CHECK IF WE NEED IT???
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_MEDIA_BY_POST, (postID,))
        return cursor.rowcount()

# Delete notification
def delete_notification_by_id(connection, notificationID):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_NOTIFICATION_BY_ID, (notificationID,))
        return cursor.rowcount()
     
def delete_notification_by_user(connection, userID):       # CHECK IF WE NEED IT???  Need to keep it if the post is deleted, how?
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_NOTIFICATION_BY_USER, (userID,))
        return cursor.rowcount()