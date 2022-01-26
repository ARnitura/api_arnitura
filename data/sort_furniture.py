from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Sort(SqlAlchemyBase):
    __tablename__ = 'sort_furniture'

    id = Column(Integer, primary_key=True)
    sort = Column(String(250), nullable=True)


