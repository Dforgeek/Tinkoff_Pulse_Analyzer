from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
from lxml import html
import re


chromedriver_path = 'D:/ML/ML_Projects/Tinkoff_Pulse_Emotion_Analyzer/Parser/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path=chromedriver_path)

driver.get(f'https://www.tinkoff.ru/invest/pulse/')

page_length = driver.execute_script("return document.body.scrollHeight")

try:
    while page_length < 50000:
        driver.execute_script(f"window.scrollTo(0, {page_length - 1000});")
        page_length = driver.execute_script("return document.body.scrollHeight")

        source_data = driver.page_source
        soup = bs(source_data, 'lxml')

        #posts = soup.find_all('div', {'class': 'PulsePostReviewBody__text_cLzKB'})
        div = driver.find_element_by_class_name('PulsePostReviewBody__text_cLzKB')
        logins = soup.find_all('div', {'class': 'PulsePostAuthor__nicknameLink_19Aca'})
        likes = soup.find_all('div', {'class': 'PulsePostBody__likes_3qcu0'})

        posts = [post.text for post in posts]
        logins = [login.text for login in logins]
        likes = [like.text.split()[0] for like in likes]

        print(len(logins), len(posts), len(likes))

        df_posts = pd.DataFrame()
        df_posts['login'] = logins
        df_posts['post'] = posts
        df_posts['likes'] = likes

        df_posts.to_csv('Parser/posts.csv', index=False)

        print('SAVED')
except Exception as E:
    print(E)




