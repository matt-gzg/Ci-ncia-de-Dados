# from bs4 import BeautifulSoup
# import requests

# url = ("https://matt-gzg.github.io/botaoSecreto/")
# html = requests.get(url).text
# soup = BeautifulSoup(html, 'html5lib')

# important_par = soup('p', {'class': 'important'})

# spans_divs = [span
#     for div in soup('div')
#     for span in div('span')]

# print(important_par)
# print(spans_divs)

from bs4 import BeautifulSoup
import requests
import re
from typing import Dict, Set

url = "http://www.house.gov/representatives"
text = requests.get(url).text
soup = BeautifulSoup(text, 'html5lib')

all_urls = [a['href']
            for a in soup('a')
            if a.has_attr('href')]

regex = r'^https?://.*\.house\.gov/?$'

assert re.match(regex, "http://joel.house.gov")
assert re.match(regex, "http://joel.house.gov/")
assert not re.match(regex, "http://joel.house.com")
assert not re.match(regex, "http://joel.house.gov/biography")

good_urls = [url for url in all_urls if re.match(regex, url)]
good_urls = list(set(good_urls))
print(len(good_urls))

press: Dict[str, Set[str]] = {}

for house in good_urls:
    html = requests.get(house).text
    soup = BeautifulSoup(html, 'html5lib')
    pr_links = [a['href'] for a in soup('a')
                if 'press' in a.text.lower()]
    # print(f"{house}: {pr_links}")
    press[house] = pr_links

def paragraph_mentions(text: str, keyword: str) -> bool:
    soup = BeautifulSoup(text, 'html5lib')
    paragraphs = [p.get_text() for p in soup('p')]

    return any(keyword.lower() in paragraph.lower()
               for paragraph in paragraphs)

for house, pr_links in press.items():
    for pr_link in pr_links:
        try:
            html = requests.get(pr_link, timeout=5).text
            if paragraph_mentions(html, 'data'):
                print(f"Encontrado em: {house}")
                break
        except requests.RequestException:
            continue