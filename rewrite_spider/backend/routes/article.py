from fastapi import APIRouter
from core.aritcle_manage import ArticleManage
from pydantic import BaseModel


article_router = APIRouter()


@article_router.get("/article/list")
async def get_article_list():
    article_manage = ArticleManage()
    article_list = await article_manage.get_article_list()
    return {
        "message": "success",
        "code": 200,
        "data": article_list,
    }


class ArticleContentRequest(BaseModel):
    title_url: str


@article_router.post("/article/content")
async def get_article_content(request: ArticleContentRequest):
    title_url = request.title_url
    article_manage = ArticleManage()
    content = await article_manage.get_article_content(title_url)
    return {
        "message": "success",
        "code": 200,
        "data": content,
    }
