import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
from loguru import logger
from services.service_sqlite import service_sqlite
import time
import json
from sqlalchemy import select
from models.aritcle_model import Article


class ArticleManage:
    def __init__(self):
        self.url = "https://www.wforum.com/news/breaking/#google_vignette"
        self.article_list = []

    async def get_html_content(self, url):
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "gbk"
            return response.text
        except Exception as e:
            print(f"请求失败: {e}")
            return None

        # try:
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(self.url, headers=headers, timeout=30) as response:
        #             return await response.text()
        # except Exception as e:
        #     print(f"请求失败: {e}")
        #     return None

    async def get_article_list(self):
        current_date = int(time.strftime("%Y%m%d"))
        results = await service_sqlite.get_all_article_data()
        if results:
            return [
                {
                    "id": article.id,
                    "current_date": article.current_date,
                    "title": article.title,
                    "content": article.content,
                    "url": article.url,
                }
                for article in results
            ]

        try:
            web_html = await self.get_html_content(self.url)
            if not web_html:
                return []
            soup = BeautifulSoup(web_html, "html.parser")
            for a in soup.find_all("a", class_="style10"):
                title = a.get_text(strip=True)
                url = a["href"]
                if url.startswith("/"):
                    url = "https://www.wforum.com" + url
                await service_sqlite.add_article_data(
                    current_date=current_date, title=title, content="", url=url
                )

            return await service_sqlite.get_all_article_data()
        except Exception as e:
            logger.error(f"获取文章列表失败: {e}")
            return []

    async def reload_article(self):
        current_date = int(time.strftime("%Y%m%d"))
        await service_sqlite.delete_table_all_data()

        try:
            web_html = await self.get_html_content(self.url)
            if not web_html:
                return []
            soup = BeautifulSoup(web_html, "html.parser")
            for a in soup.find_all("a", class_="style10"):
                title = a.get_text(strip=True)
                url = a["href"]
                if url.startswith("/"):
                    url = "https://www.wforum.com" + url
                await service_sqlite.add_article_data(
                    current_date=current_date, title=title, content="", url=url
                )
            results = await service_sqlite.get_all_article_data()
            if results:
                return [
                    {
                        "id": article.id,
                        "current_date": article.current_date,
                        "title": article.title,
                        "content": article.content,
                        "url": article.url,
                    }
                    for article in results
                ]
        except Exception as e:
            logger.error(f"获取文章列表失败: {e}")
            return []

    async def get_article_content(self, article_id, article_url):
        async with service_sqlite.async_session() as session:
            article = await session.execute(
                select(Article).where(Article.id == int(article_id))
            )
            article = article.scalar_one_or_none()
            if article.content:
                return {
                    "id": article.id,
                    "current_date": article.current_date,
                    "title": article.title,
                    "content": article.content,
                    "url": article.url,
                }

        html = await self.get_html_content(article_url)
        soup = BeautifulSoup(html, "html.parser")

        content = ""

        cont_div = soup.find("div", id="cont")
        if cont_div:
            for p in cont_div.find_all("p"):
                content += p.get_text(strip=True)

            await service_sqlite.update_article_content(article_id, content.strip())
            return {
                "id": article.id,
                "current_date": article.current_date,
                "title": article.title,
                "content": content,
                "url": article.url,
            }
        return {}

    async def delete_article_by_id(self, article_id):
        await service_sqlite.delete_table_by_id(article_id)
