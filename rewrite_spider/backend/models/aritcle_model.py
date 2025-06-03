from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    current_date = Column(Integer)
    title = Column(String(255))
    content = Column(Text)
    url = Column(String(255))
