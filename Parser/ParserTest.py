from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
from lxml import html
import re

os.chdir('D:/ML/ML_Projects/Tinkoff_Pulse_Emotion_Analyzer/Parser/')
print(os.getcwd())

post_url = "https://www.tinkoff.ru/invest/social/profile/GilmanovMedia/2477c25f-e7ea-4609-b202-15e0eaf9108a/"

response = requests.get(post_url)
response.encoding = "utf-8"
html_content = response.text

# parse the HTML content
soup_inner = bs(html_content, 'html5lib')

posts_text = []
posts_publishers = []
reactions_number = []
comments_numbers = []

post = soup_inner.find("div", {'class': ['TextLineCollapse__text_LXa9s', 'PulsePostReviewBody__text_cLzKB']})
reactions = soup_inner.find("div", class_="PulsePostReactions__countReactions_fSXGM")
comments = soup_inner.find("div", class_="PulsePostReactions__commentText_xvZNw")

post = post.text
publisher = "GilmanovMedia"
react_number = reactions.text

if comments.text == 'Комментировать':
    comments_number = 0
else:
    comments_number = comments.text

posts_text.append(post)
posts_publishers.append(publisher)
reactions_number.append(react_number)
comments_numbers.append(comments_number)

df_posts = pd.DataFrame()
df_posts['text'] = posts_text
df_posts['publisher'] = posts_publishers
df_posts['reaction'] = reactions_number
df_posts['comment'] = comments_numbers

df_posts.to_excel('posts.excel', encoding='UTF-8')

print('SAVED')
