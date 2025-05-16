import sqlalchemy
from .db_session import SqlAlchemyBase


class Requests(SqlAlchemyBase):
    __tablename__ = 'requests'
    """таблица в которую записываются все запросы из форма на сайте"""
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)