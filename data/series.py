from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Series(SqlAlchemyBase):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Айди серии товара
    id_manufacturer = Column(Integer, primary_key=True)  # Айди производителя создавшего серию
    name = Column(String(250), nullable=False)  # Название серии
    list_sort_furniture = Column(String(250), nullable=True)


