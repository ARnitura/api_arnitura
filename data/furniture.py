from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Furniture(SqlAlchemyBase):
    __tablename__ = 'furniture'

    id = Column(Integer, primary_key=True)
    color = Column(String(100), nullable=False)
    list_material = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)