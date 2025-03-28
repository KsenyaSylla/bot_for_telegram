from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MiniTest(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    onn = Column(Boolean, default=False, nullable=False)