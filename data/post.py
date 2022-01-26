from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    list_furniture = Column(String(250), nullable=False)
    photo = Column(String(250), nullable=False)
    post_name = Column(String(250), nullable=False)
    like_count = Column(String(250), nullable=True)
    favourites_count = Column(String(250), nullable=True)
    description = Column(String(500), nullable=True)
    size = Column(String(250), nullable=False)
    price = Column(String(250), nullable=False)
