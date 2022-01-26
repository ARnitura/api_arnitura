from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    date = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    count = Column(Integer)
    price = Column(String(250), nullable=False)
    list_furniture = Column(String(250), nullable=False)