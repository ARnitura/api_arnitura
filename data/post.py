from sqlalchemy import Column, Integer, String, Float
from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer_id = Column(Integer)
    list_furniture = Column(String)
    list_likes = Column(String)
    id_series = Column(String)
    id_furniture = Column(String)
    id_sort_furniture = Column(String)
    data_publication = Column(String)
    time_publication = Column(String)
