from sqlalchemy import Column, Integer, String
from app.infraestructure.db.base import Base

class ServicioModel(Base):
    __tablename__ = 'servicios'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)
