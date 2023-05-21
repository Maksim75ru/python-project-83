import os
import datetime
import psycopg2

from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def find_by_id(id_: int) -> tuple[int, str, datetime] | None:
    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id_, ))
            return cursor.fetchone()


def find_all_urls():
    urls = []
    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls")
            urls.extend(cursor.fetchall())
    return urls
