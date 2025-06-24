from fastapi import APIRouter
from core.aritcle_manage import ArticleManage
from pydantic import BaseModel


article_router = APIRouter()


@article_router.get("/list")
async def get_article_list():
    article_manage = ArticleManage()
    article_list = await article_manage.get_article_list()
    return {
        "message": "success",
        "code": 200,
        "data": article_list,
    }


@article_router.post("/reload")
async def reload_article():
    article_manage = ArticleManage()
    article_list = await article_manage.reload_article()
    return {
        "message": "success",
        "code": 200,
        "data": article_list,
    }


class ArticleContentRequest(BaseModel):
    article_id: int
    article_url: str


@article_router.post("/content")
async def get_article_content(request: ArticleContentRequest):
    article_id = request.article_id
    article_url = request.article_url
    article_manage = ArticleManage()
    content = await article_manage.get_article_content(article_id, article_url)
    return {
        "message": "success",
        "code": 200,
        "data": content,
    }


class DeleteArticleRequest(BaseModel):
    url: str


@article_router.delete("/delete")
async def delete_article_by_url(request: DeleteArticleRequest):
    article_manage = ArticleManage()
    await article_manage.delete_article_by_url(request.url)
    return {
        "message": "success",
        "code": 200,
    }
