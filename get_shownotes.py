import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    """
    发送HTTP请求获取页面内容
    :param url: 页面URL
    :return: 页面内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

def parse_page_content(html_content):
    """
    使用BeautifulSoup解析页面内容
    :param html_content: 页面HTML内容
    :return: 解析后的BeautifulSoup对象
    """
    return BeautifulSoup(html_content, 'html.parser')

def get_page_title(soup):
    """
    提取页面标题
    :param soup: 解析后的BeautifulSoup对象
    :return: 页面标题
    """
    return soup.title.string if soup.title else None

def get_shownotes(soup):
    """
    提取shownotes部分
    :param soup: 解析后的BeautifulSoup对象
    :return: shownotes内容
    """
    article = soup.find('article')
    if article:
        return article.get_text()
    else:
        return None

def convert_to_markdown(text):
    """
    将文本内容转换为Markdown格式
    :param text: 原始文本内容
    :return: 转换后的Markdown文本
    """
    markdown_text = ''
    for tag in BeautifulSoup(text, 'html.parser').descendants:
        if tag.name == 'a' and 'href' in tag.attrs:
            link_text = tag.get_text()
            link_url = tag['href']
            markdown_text += f'[{link_text}]({link_url})\n'
        elif tag.name == 'p':
            markdown_text += '\n' + tag.get_text() + '\n'
        elif tag.name is None and tag.string:
            markdown_text += tag.string + '\n'
    return markdown_text

def get_page_info(url):
    """
    获取页面的标题和shownotes内容，并将shownotes转换为Markdown格式
    :param url: 页面URL
    :return: 页面标题和shownotes内容（Markdown格式）
    """
    html_content = get_page_content(url)
    if html_content:
        soup = parse_page_content(html_content)
        page_title = get_page_title(soup)
        shownotes = get_shownotes(soup)
        if shownotes:
            shownotes_markdown = convert_to_markdown(shownotes)
            return page_title, shownotes_markdown
        else:
            return page_title, None
    else:
        return None, None

# 示例用法
url = input("请输入小宇宙文章链接: ")
page_title, shownotes_markdown = get_page_info(url)
if page_title and shownotes_markdown:
    print(f"Page Title: {page_title}")
    print(f"Shownotes:\n{shownotes_markdown}")
else:
    print("获取页面信息失败")
