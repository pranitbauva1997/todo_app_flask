from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable = False)
    date = Column(String(255), nullable = False)

engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
