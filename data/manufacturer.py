from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Manufacturer(SqlAlchemyBase):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    avatar_photo = Column(String(250), nullable=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    mail = Column(String(250), nullable=True)
    phone_number = Column(String(250), nullable=True)
    site = Column(String(250), nullable=True)
    list_likes = Column(Integer, nullable=False, default='0')
    list_favourites = Column(Integer, nullable=False, default='0')
    list_products = Column(Integer, nullable=False, default='0')
    list_orders = Column(Integer, nullable=False, default='0')
