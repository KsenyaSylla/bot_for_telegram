from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Defect(Base):
    __tablename__ = "defects"

    defect = Column(Integer, primary_key=True, index=True)  # ID дефекта
    status = Column(String, nullable=False)  # Статус дефекта
    history = Column(JSONB, nullable=True)  # История изменений (JSONB)