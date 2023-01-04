from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
from lxml import html
import re
import sys

chromedriver_path = '/chromedriver_win32/chromedriver.exe'
chrome_service = ChromeService(executable_path=chromedriver_path)
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service)

driver.get(f'https://www.tinkoff.ru/invest/pulse/')

page_length = driver.execute_script("return document.body.scrollHeight")

posts_text = []
posts_publishers = []
reactions_number = []
comments_numbers = []
post_all = 0
while page_length < 50000:
    driver.execute_script(f"window.scrollTo(0, {page_length - 500});")
    page_length = driver.execute_script("return document.body.scrollHeight")

    source_data = driver.page_source
    soup = bs(source_data, 'lxml')

    post_all = soup.find_all("div", {'data-qa-tag': "PulsePost"})

for i in post_all:
    print(i.attrs)
    print("post_ID: " + i['data-post-id'])
    author = i.find('a', {'data-qa-type': "uikit/link"}, source=i)
    print("AuthorLink: " + author['href'] + "//n")
    post_url = "https://www.tinkoff.ru" + author['href'] + i['data-post-id'] + '/'

    response = requests.get(post_url)
    response.encoding = 'utf-8'
    html_content = response.text
    # print("HTML CONTENT: ", html_content)
    # parse the HTML content
    soup_inner = bs(html_content, 'html.parser')
    # print(soup_inner.prettify())

    post = soup_inner.find("div", {'class': ['TextLineCollapse__text_LXa9s', 'PulsePostReviewBody__text_cLzKB']})
    reactions = soup_inner.find("div", class_="PulsePostReactions__countReactions_fSXGM")
    comments = soup_inner.find("div", class_="PulsePostReactions__commentText_xvZNw")

    post = post.text
    # print(post)
    publisher = author['href'].split('/')[4]
    react_number = reactions.text

    if comments.text == 'Комментировать':
        comments_number = 0
    else:
        comments_number = comments.text

    posts_text.append(post)
    posts_publishers.append(publisher)
    reactions_number.append(react_number)
    comments_numbers.append(comments_number)

    print("SPECIFIC POST WAS READ\n")

print("SCROLLING\nSCROLLING\n")

df_posts = pd.DataFrame()
df_posts['text'] = posts_text
df_posts['publisher'] = posts_publishers
df_posts['reaction'] = reactions_number
df_posts['comment'] = comments_numbers
df_posts = df_posts.drop_duplicates()
df_posts.to_excel('posts.xlsx', encoding='UTF-8')

print('SAVED')
