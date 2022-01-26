from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Type(SqlAlchemyBase):
    __tablename__ = 'type_furniture'

    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=True)


