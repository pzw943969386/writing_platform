import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp


class ArticleManage:
    def __init__(self):
        self.url = "https://www.wforum.com/news/breaking/#google_vignette"
        self.article_list = []

    def get_article_title(self):
        ...

    async def get_html_content(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        try:
            async with aiohttp.CilentSession() as session:
                async with session.get(self.url, headers=headers, timeout=10) as response:
                    response.encoding = 'gbk'
                    return await response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    async def get_article_list(self):
        web_html = await self.get_html_content()
        soup = BeautifulSoup(web_html, 'html.parser')
        results = []
        for a in soup.find_all('a', class_='style10'):
            title = a.get_text(strip=True)
            url = a['href']
            if url.startswith('/'):
                url = 'https://www.wforum.com' + url
            results.append((title, url))
        return results

    def get_article_content(self, title_url):
        html = self.get_html_content(title_url)
        soup = BeautifulSoup(html, 'html.parser')
        title_span = soup.find('span', class_='STYLE55')
        title = title_span.get_text(strip=True)
        content = ""
        cont_div = soup.find('div', id='cont')
        if cont_div:
            for p in cont_div.find_all('p'):
                content += p.get_text(strip=True)
        else:
            return "未找到正文内容"
        return content
