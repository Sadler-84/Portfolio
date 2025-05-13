from flask import Flask, render_template
from data import db_session
from data.places import Places
import sqlite3
import requests
import io
import shutil
import os
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SECRET_KEY'] = "sadler_portfolio"



def get_images():
    # информация для API Yandex Maps
    API_KEY = ""

    folder_path = "static/img"

    # Удаление старых изображений
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Ошибка при удалении {file_path}: {e}")

    # Подключение к базе данных
    conn = sqlite3.connect('db/blogs.db')
    cursor = conn.cursor()

    # Получение количества записей в таблице places
    cursor.execute("SELECT COUNT(*) FROM places")
    total_records = cursor.fetchone()[0]

    for i in range(1, total_records + 1):
        cursor.execute("SELECT coord FROM places WHERE id = ?", (i,))
        record = cursor.fetchone()
        if record:
            try:
                coord_str = record[0]  # строка вида "84.947649, 56.484645"
                longitude, latitude = coord_str.split(", ")

                # Параметры запроса к Yandex Static Maps API
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
                    filename = os.path.join(folder_path, f"map_{i}.png")
                    with open(filename, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    print(f"Сохранена карта для места {i}: {filename}")
                else:
                    print(f"Ошибка загрузки карты для места {i}: код {response.status_code}")

            except Exception as e:
                print(f"Ошибка при обработке места {i}: {e}")

    conn.close()



@app.route("/")
@app.route("/main")
def index():
    conn = sqlite3.connect('db/blogs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, coord, name, description FROM places")
    places = cursor.fetchall()
    conn.close()
    return render_template('main.html', places=places)


def main():
    db_session.global_init("db/blogs.db")
    get_images()
    app.run(port=8080)


    # Изначальное добавление в БД значимых мест

    # place = Places()
    # place.name = "Томск - RoboCup"
    # place.coord = "84.947649, 56.484645"
    # place.description = "В Томске проводились крупные соревнования RoboCup в которых я со своей командой принял участие."
    # place2 = Places()
    # place2.name = "Сириус - T2C"
    # place2.coord = "39.950671, 43.414729"
    # place2.description = """В Сириусе проходили ежегодные соревнования T2C в которых альянсы решают разные задачи"""
    # db_sess = db_session.create_session()
    # db_sess.add(place)
    # db_sess.add(place2)
    # db_sess.commit()

    # Позднее при развитии проекта можно будет добавлять новые значимые места



if __name__ == '__main__':
    main()