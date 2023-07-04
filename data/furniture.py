from sqlalchemy import Column, Integer, String, Float
from .db_session import SqlAlchemyBase


class Furniture(SqlAlchemyBase):
    __tablename__ = 'furniture'

    id = Column(Integer, primary_key=True)
    articul = Column(String(255), nullable=True)
    manufacturer_id = Column(Integer)
    name = Column(String(255))
    type_furniture = Column(Integer)
    photo_furniture = Column(String(250))
    description = Column(String(255))
    width = Column(String(255))
    length = Column(String(255))
    height = Column(String(255))
    model = Column(String(250))
    price = Column(Float(255))
    id_material = Column(String(255))