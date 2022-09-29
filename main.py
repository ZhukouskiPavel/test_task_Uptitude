"""
Take a user input of website URL (e.g., https://www.imdb.com)
2) Extract different attributes like status code, encoding, elapsed
3) Extract all links
4) Combine the data into a table (e.g., pandas DataFrame) and display the content in a readable format
Optional: Check if the website contains the specific word (also from user input)
"""

from typing import Any
from urllib.parse import urlparse, urljoin

import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd


internal_urls = set()


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_content_site(url: str):
    try:
        page = requests.get(url)
        return page
    except Exception as ext:
        print(ext, ', try again:')
        url_get_site(input('enter url site: '))


def url_get_site(url : str) -> pandas.DataFrame | None :
    page = get_content_site(url)
    if page is None:
        return None
    soup = BeautifulSoup(page.content , 'html.parser')
    all_links = []
    links = soup.findAll('a')
    for ahref in links:
        text = ahref.text
        if not text :
            text = 'None text'
        href = ahref.get('href')
        href = href.strip() if href is not None else ''
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid_url(href):
            continue
        if href in internal_urls:
            continue
        internal_urls.add(href)
        all_links.append({"Text": text, "href": href})

    pd.set_option('display.max_rows', None)
    data = pd.DataFrame(all_links)
    print("status code: ", page.status_code)
    print("encoding: ", page.encoding)
    print("elapsed: ", page.elapsed)
    print(data)
    word_search(input('enter word : '), page)
    return data


def word_search(word : str, page: Any) -> bool:
    page = page
    if page is None:
        return False
    if word in page.text:
        print(f'Found the word "{word}" on page "{page.url}"')
        return True
    else:
        print(f'Word "{word}" not found on page "{page.url}"')
        return False


if __name__ == "__main__":
    url_get_site(input('enter url site: '))
