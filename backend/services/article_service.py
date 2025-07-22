from bs4 import BeautifulSoup
import aiohttp
import chardet
from loguru import logger
from ..datebase.sqlite import sqlite_service
from ..models.article_model import Article
import time


class ArticleService:
    def __init__(self):
        self.base_url = "https://www.wforum.com"
        self.news_url = f"{self.base_url}/news/breaking"
        self.article_list = []

    async def get_html_content(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    content = await response.read()
                    detected = chardet.detect(content)
                    encoding = detected["encoding"] or "utf-8"
                    return content.decode(encoding, errors="ignore")
        except Exception as e:
            logger.error(f"请求失败: {e}")
            return None

    @staticmethod
    def _format_articles(articles: list[Article]) -> list[dict]:
        return [
            {
                "id": article.id,
                "current_date": article.current_date,
                "title": article.title,
                "content": article.content,
                "url": article.url,
            }
            for article in articles
        ]

    async def _fetch_and_save_articles_from_web(self) -> bool:
        try:
            html = await self.get_html_content(self.news_url)
            if not html:
                return False

            soup = BeautifulSoup(html, "html.parser")
            current_date = int(time.strftime("%Y%m%d"))

            for a_tag in soup.find_all("a", class_="style10"):
                title = a_tag.get_text(strip=True)
                url = a_tag.get("href")
                if url and url.startswith("/"):
                    url = self.base_url + url

                if title and url:
                    await sqlite_service.add_article_data(
                        current_date=current_date, title=title, content="", url=url
                    )
            return True
        except Exception as e:
            logger.error(f"Failed to scrape and save articles: {e}")
            return False

    async def get_article_list(self):
        results = await sqlite_service.get_all_article_data()
        if results:
            return self._format_articles(results)

        success = await self._fetch_and_save_articles_from_web()
        if not success:
            return []

        new_results = await sqlite_service.get_all_article_data()
        return self._format_articles(new_results)

    async def reload_article(self):
        await sqlite_service.delete_table_all_data()

        success = await self._fetch_and_save_articles_from_web()
        if not success:
            return []

        new_results = await sqlite_service.get_all_article_data()
        return self._format_articles(new_results)

    async def get_article_content(self, article_id, article_url):
        db_article = await sqlite_service.get_article_by_id(article_id)

        if not db_article:
            return None

        if db_article.content:
            return self._format_articles([db_article])[0]

        html = await self.get_html_content(article_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        content_div = soup.find("div", id="cont")

        if not content_div:
            return None

        full_content = "".join(
            p.get_text(strip=True) for p in content_div.find_all("p")
        )

        await sqlite_service.update_article_content(article_id, full_content.strip())
        db_article.content = full_content.strip()

        return self._format_articles([db_article])[0]

    async def delete_article_by_id(self, article_id):
        await sqlite_service.delete_table_by_id(article_id)

    async def get_article_content_by_url(self, url):
        html = await self.get_html_content(url)
        if not html:
            return ""

        soup = BeautifulSoup(html, "html.parser")
        content_div = soup.find("div", id="cont")
        if content_div:
            return "".join(p.get_text(strip=True) for p in content_div.find_all("p"))
        return ""


article_service = ArticleService()
