import sqlalchemy
from .db_session import SqlAlchemyBase


class Places(SqlAlchemyBase):
    __tablename__ = 'places'
    """Таблица для "Интересных мест" в ней записывается название, id, координаты и описание события"""
    #позже из этой таблицы бертуся данные по координатам для получения изображения из Yandex API

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    coord = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)