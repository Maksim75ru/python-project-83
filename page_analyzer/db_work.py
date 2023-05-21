import os
import datetime
from typing import Any, List, Tuple

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


def find_checks(url_id: int) -> list[tuple[Any, ...]]:
    url_checks = []

    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s\
                           ORDER BY id DESC",
                           (url_id, ))
            url_checks.extend(cursor.fetchall())

    return url_checks


def find_checks(url_id: int) -> list[tuple[Any, ...]]:
    url_checks = []

    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s\
                           ORDER BY id DESC",
                           (url_id, ))
            url_checks.extend(cursor.fetchall())

    return url_checks
