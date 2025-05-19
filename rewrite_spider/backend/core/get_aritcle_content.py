import os
import aiohttp
from loguru import logger
from bs4 import BeautifulSoup

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