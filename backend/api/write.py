from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from ..services.write_service import write_service

write_router = APIRouter()


class ArticleWriteRequest(BaseModel):
    article_type: str
    article_content: str


@write_router.post("/article_write")
async def article_write(request: ArticleWriteRequest):
    article_type = request.article_type
    article_content = request.article_content
    try:

        async def generate_article():
            async for chunk in write_service.write_article(
                article_type, article_content
            ):
                yield chunk

        return StreamingResponse(generate_article(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"write article error: {e}")
