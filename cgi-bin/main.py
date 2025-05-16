from flask import Flask, render_template, request, redirect
from data import db_session
from data.places import Places
from data.requests import Requests
import sqlite3
import requests
import shutil
import os
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SECRET_KEY'] = "sadler_portfolio"

def get_images():
    """Получение изображений "Интересных мест" из БД places"""
    API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    folder_path = "static/img"

    # Подключение к БД
    conn = sqlite3.connect('db/blogs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, coord FROM places")
    places = cursor.fetchall()
    conn.close()

    for place_id, coord_str in places:
        filename = os.path.join(folder_path, f"map_{place_id}.png")

        # Пропустить, если файл уже существует
        if os.path.exists(filename):
            print(f"Карта для места {place_id} уже существует, пропускаем.")
            continue

        try:
            longitude, latitude = coord_str.split(", ")
            params = {
                'll': f"{longitude},{latitude}",
                'z': 12,
                'size': "650,450",
                'l': 'map',
                'apikey': API_KEY
            }
            url = f"https://static-maps.yandex.ru/1.x/?{urlencode(params)}"
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                with open(filename, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(f"Сохранена карта для места {place_id}: {filename}")
            else:
                print(f"Ошибка загрузки карты для места {place_id}: код {response.status_code}")
        except Exception as e:
            print(f"Ошибка при обработке места {place_id}: {e}")

@app.route("/")
@app.route("/main")
def index():
    """Главная страница на которой находится сайт"""

    #подключение ка бызе данных
    conn = sqlite3.connect('db/blogs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, coord, name, description FROM places")
    places = cursor.fetchall()
    conn.close()

    # Получаем изображения map_*.png
    image_dir = os.path.join("static", "img")
    images = sorted([
        f for f in os.listdir(image_dir)
        if f.startswith("map_") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ])

    return render_template('main.html', places=places, images=images)


@app.route("/add_request", methods=["POST"])
def add_request():
    """Обработка записей по форме и запись в БД requests"""
    db_sess = db_session.create_session()
    new_request = Requests()
    new_request.name = request.form["name"]
    new_request.email = request.form["email"]
    new_request.description = request.form["description"]
    db_sess.add(new_request)
    db_sess.commit()
    return redirect("/")

def main():
    db_session.global_init("db/blogs.db")
    get_images()
    app.run(port=8080)

if __name__ == '__main__':
    main()
