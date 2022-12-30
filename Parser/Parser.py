from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
from lxml import html
import re


chromedriver_path = '/chromedriver_win32/chromedriver.exe'
chrome_service = ChromeService(executable_path=chromedriver_path)
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service)

driver.get(f'https://www.tinkoff.ru/invest/pulse/')

page_length = driver.execute_script("return document.body.scrollHeight")


try:
    while page_length < 50000:
        driver.execute_script(f"window.scrollTo(0, {page_length - 1000});")
        page_length = driver.execute_script("return document.body.scrollHeight")

        source_data = driver.page_source
        soup = bs(source_data, 'lxml')

        post_click = soup.find_all("div", {'class': ["PulseReviewAndNewsBody__title_SzTYH",
                                                     "PulsePostBody__clickable_ygAE0"]})

        for post in post_click:
            print(type(post))
            if post.is_displayed():
                print("disp")
            post.click()
            driver.implicitly_wait(10)

            post_text = post.text
            print("OK")
            driver.back()


        posts = soup.find_all("div", {'class': ["TextLineCollapse__text_LXa9s",
                                                "PulseReviewAndNewsBody__announce_tXACb",
                                                "PulsePostReviewBody__text_cLzKB"]})
        publisher = soup.find_all('div', {'class': 'PulsePostAuthor__nicknameLink_pmYg4'})
        reactions = soup.find_all("div", class_="PulsePostReactions__countReactions_vtahc")
        comments = soup.find_all("div", class_="PulsePost__commentText_WiLNw")

        posts = [post.text for post in posts]
        publishers = [login.text for login in publisher]
        reactions_number = [int(reaction.text) for reaction in reactions]

        comments_number = []
        for comment in comments:
            if comment.text == 'Комментировать':
                comments_number.append(0)
            else:
                comments_number.append(int(comment.text))

        df_posts = pd.DataFrame()
        df_posts['text'] = posts
        df_posts['publisher'] = publishers
        df_posts['reactions'] = reactions_number
        df_posts['comments'] = comments_number

        df_posts.to_csv('Parser/posts.csv', index=False)

        print('SAVED')
except Exception as E:
    print(E)




