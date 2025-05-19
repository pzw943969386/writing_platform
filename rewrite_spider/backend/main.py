from fastapi import FastAPI
from core.aritcle_manage import ArticleManage
from loguru import logger
from pydantic import BaseModel

app = FastAPI()

@app.get("/get_article_title")
def get_article_title():
    article_manage = ArticleManage()
    article_list = article_manage.get_article_list()
    return {"article_list": article_list}

class ArticleContent(BaseModel):
    title_url: str

@app.get("/get_article_content")
def get_article_content(article_content: ArticleContent):
    article_manage = ArticleManage()
    content = article_manage.get_article_content(article_content.title_url)
    return {"content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)