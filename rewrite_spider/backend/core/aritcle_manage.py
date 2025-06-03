import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
from loguru import logger
from services.service_sqlite import service_sqlite
import time


class ArticleManage:
    def __init__(self):
        self.url = "https://www.wforum.com/news/breaking/#google_vignette"
        self.article_list = []

    def get_article_title(self): ...
    
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
        results = await service_sqlite.get_article_list(current_date)
        if results:
            return results

        try:
            web_html = await self.get_html_content(self.url)
            if not web_html:
                return []
            soup = BeautifulSoup(web_html, "html.parser")
            results = []
            for a in soup.find_all("a", class_="style10"):
                title = a.get_text(strip=True)
                url = a["href"]
                if url.startswith("/"):
                    url = "https://www.wforum.com" + url
                results.append({"title": title, "url": url})
                await service_sqlite.save_article_by_current_date(current_date, title, "", url)
            return results
        except Exception as e:
            return []

    async def get_article_content(self, title_url):
        content = await service_sqlite.get_article_content_by_url(title_url)
        if content:
            return content
        
        html = await self.get_html_content(title_url)
        soup = BeautifulSoup(html, "html.parser")
        title_span = soup.find("span", class_="STYLE55")
        title = title_span.get_text(strip=True)
        content = ""
        cont_div = soup.find("div", id="cont")
        if cont_div:
            for p in cont_div.find_all("p"):
                content += p.get_text(strip=True)
                await service_sqlite.update_article_by_url(title_url, content)
        else:
            return "未找到正文内容"
        return content
