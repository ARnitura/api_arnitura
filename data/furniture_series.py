from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Series(SqlAlchemyBase):
    __tablename__ = 'series_furniture'

    id = Column(Integer, primary_key=True)
    id_manufacturer = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    list_type_furniture = Column(String(250), nullable=True)
    list_sort_furniture = Column(String(250), nullable=True)


