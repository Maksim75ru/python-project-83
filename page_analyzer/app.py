import os
import requests
from datetime import datetime

from psycopg2.extras import NamedTupleCursor
from werkzeug import Response

from .db_work import get_connection, find_by_id, find_all_urls, find_checks

from .url import validate_url, normalize_url
from dotenv.main import load_dotenv
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    get_flashed_messages,
    url_for,
)


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/urls', methods=['POST'])
def urls_post() -> tuple[str, int] | Response:
    url_from_request = request.form.to_dict().get('url', '')
    errors = validate_url(url_from_request)

    if 'Not valid url' in errors:
        flash('Некорректный URL', 'alert-danger')
        if 'No url' in errors:
            flash('URL обязателен', 'alert-danger')
        return render_template('index.html'), 422

    new_url = normalize_url(url_from_request)

    with get_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("INSERT INTO urls (name, created_at)\
                            VALUES (%s, %s) RETURNING id",
                           (new_url,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            url_info = cursor.fetchone()
            url_id = url_info.id
            flash('Страница успешно добавлена', 'alert-success')

    return redirect(url_for('get_one_url', id=url_id))


@app.get("/urls/<int:id>")
def get_one_url(id: int):
    url_info = find_by_id(id)

    if url_info is None:
        flash("Такой страницы не существует", "alert-warning")
        return redirect(url_for("index"), code=404)

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        "show_one_url.html",
        id=url_info.id,
        name=url_info.name,
        created_at=url_info.created_at,
        messages=messages,
        checks=find_checks(id),
    )


@app.get("/urls")
def get_urls():
    urls = find_all_urls()
    return render_template("urls.html", urls=urls)


@app.post("/urls/<int:id>/checks")
def check_url(id: int):
    url_info = find_by_id(id)

    try:
        with requests.get(url_info.name) as response:
            status_code = response.status_code  # noqa
            response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return render_template(
            'show_one_url.html',
            id=id,
            name=url_info.name,
            created_at=url_info.created_at,
            checks=find_checks(id)
        ), 422

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO url_checks \
                                (url_id, status_code, created_at)\
                           VALUES (%s, %s, %s)",
                           (id,
                            status_code,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            ))
            flash('Страница успешно проверена', 'alert-success')

    return redirect(url_for('get_one_url', id=id))
