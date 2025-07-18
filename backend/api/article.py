from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models.article_model import ArticleResponse, ArticleContentResponse
from ..services.article_service import article_service

article_router = APIRouter()


@article_router.get("/list/{type}")
async def get_article_list(type: str):
    try:
        if type != "breaking":
            raise HTTPException(status_code=400, detail="type 参数错误")

        article_list = await article_service.get_article_list()
        return ArticleResponse(message="success", code=200, data=article_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文章列表失败: {e}")


@article_router.post("/reload")
async def reload_article():
    try:
        article_list = await article_service.reload_article()
        return ArticleResponse(message="success", code=200, data=article_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文章列表失败: {e}")


class ArticleContentRequest(BaseModel):
    article_id: int
    article_url: str


@article_router.post("/content")
async def get_article_content(request: ArticleContentRequest):
    article_id = request.article_id
    article_url = request.article_url
    try:
        content = await article_service.get_article_content(article_id, article_url)
        return ArticleContentResponse(message="success", code=200, data=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文章内容失败: {e}")


class DeleteArticleRequest(BaseModel):
    url: str


@article_router.delete("/delete")
async def delete_article_by_url(request: DeleteArticleRequest):
    try:
        await article_service.delete_article_by_url(request.url)
        return ArticleResponse(message="success", code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文章失败: {e}")


class ArticleContentByUrlRequest(BaseModel):
    url: str


@article_router.post("/content/url")
async def get_article_content_by_url(request: ArticleContentByUrlRequest):
    try:
        content = await article_service.get_article_content_by_url(request.url)
        return ArticleContentResponse(message="success", code=200, data=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文章内容失败: {e}")
