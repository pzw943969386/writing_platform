import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from loguru import logger
import os

class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

def load_md_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def replace_placeholders(file_path, data):
    template = load_md_template(file_path)
    return template.format_map(SafeDict(data))

def get_html(url):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gbk'
        return response.text
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def parse_aritcle_html(title, html):
    soup = BeautifulSoup(html, 'html.parser')
    title_span = soup.find('span', class_='STYLE55')
    title = title_span.get_text(strip=True)
    content = ""
    cont_div = soup.find('div', id='cont')
    if cont_div:
        for p in cont_div.find_all('p'):
            content += p.get_text(strip=True)
    else:
        print("未找到正文内容")
    
    if not os.path.exists("article"):
        os.makedirs("article")
    
    template_path = "md/new.md"
    data = {
        "new_title": title,
        "new_content": content
    }
    new_content = replace_placeholders(template_path, data)
    
    with open(f"article/{title}.txt", "w", encoding="utf-8") as f:
        f.write(new_content)
    logger.info(f"已保存文章: {title}")

def get_titles_and_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    # 找到所有 class 为 style10 的 a 标签
    for a in soup.find_all('a', class_='style10'):
        title = a.get_text(strip=True)
        url = a['href']
        # 如果是相对路径，拼接成完整 url
        if url.startswith('/'):
            url = 'https://www.wforum.com' + url
        results.append((title, url))
    return results


def main():
    base_url = 'https://www.wforum.com/news/breaking/#google_vignette'
    html = get_html(base_url)
    # print(html)
    titles_and_urls = get_titles_and_urls(html)
    for title, url in titles_and_urls[:10]:
        try:
            aircle_html = get_html(url)
            # print(aircle_html)
            parse_aritcle_html(title, aircle_html)
        except Exception as e:
            print(f"请求失败: {e}")


if __name__ == '__main__':
    main()