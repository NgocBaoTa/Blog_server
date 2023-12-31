import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_url)

@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally: 
        pool.putconn(connection)