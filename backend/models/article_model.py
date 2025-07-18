from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ConfigDict
from typing import Optional

Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    current_date = Column(Integer)
    title = Column(String(255))
    content = Column(Text)
    url = Column(String(255))

class ArticleData(BaseModel):
    id: int
    current_date: int
    title: str
    content: Optional[str] = None
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ArticleResponse(BaseModel):
    message: str
    code: int
    data: list[ArticleData]

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"example": {"message": "success", "code": 200, "data": []}},
    )


class ArticleContentResponse(BaseModel):
    message: str
    code: int
    data: ArticleData

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"message": "success", "code": 200, "data": {
            "id": 0,
            "current_date": 0,
            "title": "unknown",
            "content": "unknown",
            "url": "unknown"
        }}},
    )
