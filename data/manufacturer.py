from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Manufacturer(SqlAlchemyBase):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    inn = Column(String, nullable=False)
    avatar_photo = Column(String(250), nullable=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    mail = Column(String(250), nullable=True)
    data_reg = Column(String(250), nullable=False)
    time_reg = Column(String(250), nullable=False)
    phone_number = Column(String(250), nullable=True)
    password = Column(String(250), nullable=False)
    site = Column(String(250), nullable=True)
    list_likes = Column(Integer, nullable=False, default='0')
    list_favourites = Column(Integer, nullable=False, default='0')
    list_products = Column(Integer, nullable=False, default='0')
    list_orders = Column(Integer, nullable=False, default='0')
    is_admin = Column(Integer, nullable=False, default='0')
