import os
import datetime
from typing import Any
import logging
import psycopg2

from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def find_by_id(id_: int) -> (int, str, datetime, None):
    logging.info("Start find_by_id")
    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id_,))
            return cursor.fetchone()


def find_by_name(name: str) -> (int, str, datetime, None):
    logging.info("Start find_by_name")
    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (name,))
            return cursor.fetchone()


def find_all_urls() -> list:
    logging.info("Start find_all_urls")
    urls = []
    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "SELECT urls.id, urls.name, \
                MAX(url_checks.created_at) AS check_time, \
                url_checks.status_code FROM urls \
                LEFT JOIN url_checks \
                ON urls.id = url_checks.url_id \
                GROUP BY urls.id, url_checks.status_code \
                ORDER BY urls.id DESC;"
            )
            urls.extend(cursor.fetchall())
    return urls


def find_checks(url_id: int) -> list[tuple[Any, ...]]:
    logging.info("Start find_checks")
    url_checks = []

    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "SELECT * FROM url_checks WHERE url_id = %s\
                ORDER BY id DESC",
                (url_id,),
            )
            url_checks.extend(cursor.fetchall())

    return url_checks
