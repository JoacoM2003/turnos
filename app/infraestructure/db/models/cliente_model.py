from sqlalchemy import Column, Integer, String
from app.infraestructure.db.base import Base

class ClienteModel(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
