from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    patronymic = Column(String(250), nullable=False)
    avatar = Column(String(250), nullable=True)
    phone = Column(String(250), nullable=False)
    mail = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    login = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    data_reg = Column(String(250), nullable=False)
    time_reg = Column(String(250), nullable=False)
    list_favourites = Column(String(250), nullable=False)
    list_orders = Column(String(250), nullable=False)