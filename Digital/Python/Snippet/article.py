import requests
import os
from typing import List
from unicodedata import normalize
from lxml import etree


def article_attribute(url: str, path: str) -> List[str]:
    """获取文章属性

    主要针对具有文章索引页的情形，获取文章标题或URL。

    Args:
        url (str): 文章索引页URL
        path (str): xpath函数的查询参数

    Returns:
        List[str]: 文章标题或URL
    """
    res = etree.HTML(requests.get(url).text)
    return res.xpath(path)


def article_content(url: str, path: str) -> List[str]:
    """获取文章内容

    Args:
        url (str): 文章URL
        path (str): xpath函数的查询参数

    Returns:
        List[str]: 文章内容列表
    """
    res = etree.HTML(requests.get(url).text)
    content = res.xpath(path)
    for i, v in enumerate(content):
        s = normalize("NFKD", ''.join(v.itertext())).replace(' ', '')
        content[i] = s.replace('\r\n', '\n').replace('\n\n', '\n')
    return list(filter(None, content))


def get_folder(folder: str) -> str:
    """获取文件夹，若不存在则创建

    Args:
        folder (str): 文件夹名称

    Returns:
        str: 文件夹绝对路径
    """
    if not os.path.exists(folder):
        os.mkdir(folder)
    return os.path.abspath(folder) + '/'


def to_file(fullname: str, url: str, path: str, mode: str = 'w') -> None:
    """获取文章内容并写入文件

    Args:
        fullname (str): [description]
        url (str): 文章URL
        path (str): xpath函数的查询参数
        mode (str, optional): 写入文件的模式，缺省值为 'w'.
    """
    content = article_content(url, path)
    with open(fullname, mode, encoding='utf-8') as f:
        f.write('\n'.join(content))
