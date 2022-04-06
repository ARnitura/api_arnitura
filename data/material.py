from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Material(SqlAlchemyBase):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    color = Column(String(250), nullable=False)
    texture = Column(String(250), nullable=False)