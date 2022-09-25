from sqlalchemy import Column, Integer, String, DateTime, func
import datetime
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=5), name='surgut')), nullable=False)
    name = Column(String(250))
    phone = Column(String(250), nullable=False)
    mail = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    json_order = Column(String(5000), nullable=False)