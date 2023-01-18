from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
import DateParser


print(os.getcwd())
chromedriver_path = 'chromedriver_win32/chromedriver.exe'

# add options to driver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")

driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(f'https://www.tinkoff.ru/invest/pulse/')

page_length = driver.execute_script("return document.body.scrollHeight")

posts_id = []
publish_date = []
posts_text = []
posts_publishers = []
reactions_number = []
comments_numbers = []
unique_id_set = set()

while page_length < 5000:
    driver.execute_script(f"window.scrollTo(0, {page_length - 1000});")
    page_length = driver.execute_script("return document.body.scrollHeight")

source_data = driver.page_source
soup = bs(source_data, 'lxml')
post_all = soup.find_all("div", {'data-qa-tag': "PulsePost"})
post_found = len(post_all)
print("Posts found: ", post_found)

for i in post_all:
    #print(i.attrs)
    post_id = i['data-post-id']
    print("post_ID: " + post_id)
    author = i.find('a', {'data-qa-type': "uikit/link"}, source=i)
    print("AuthorLink: " + author['href'])
    post_url = "https://www.tinkoff.ru" + author['href'] + post_id + '/'
    unique_id_set.add(post_id)

    try:
        response = requests.get(post_url)
    except requests.exceptions.Timeout:
        print("Timeout error on this URL: ", post_url)
    except requests.exceptions.TooManyRedirects:
        print("TooManyRedirects error on this URL: ", post_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    response.encoding = 'utf-8'
    html_content = response.text
    soup_inner = bs(html_content, 'html.parser')

    post = soup_inner.find("div", {'class': ['TextLineCollapse__text_LXa9s', 'PulsePostReviewBody__text_cLzKB']})
    date = soup_inner.find("div", class_="PulsePostAuthor__inserted_OW9vN")
    reactions = soup_inner.find("div", class_="PulsePostReactions__countReactions_fSXGM")
    comments = soup_inner.find("div", class_="PulsePostReactions__commentText_xvZNw")

    post = post.text
    date = DateParser.string_to_date(date.text)
    print("Post date:" + str(date) + "\n")
    publisher = author['href'].split('/')[4]
    react_number = reactions.text

    if comments.text == 'Комментировать':
        comments_number = 0
    else:
        comments_number = comments.text

    posts_id.append(post_id)
    publish_date.append(date)
    posts_text.append(post)
    posts_publishers.append(publisher)
    reactions_number.append(react_number)
    comments_numbers.append(comments_number)

    print("POST WAS SCRAPED\n")

print("Post was found:", post_found)
print("Unique posts:", len(unique_id_set))
print("Posts scraped:", len(posts_id))

df_posts = pd.DataFrame()
df_posts['id'] = posts_id
df_posts['date'] = publish_date
df_posts['text'] = posts_text
df_posts['publisher'] = posts_publishers
df_posts['reaction'] = reactions_number
df_posts['comment'] = comments_numbers
df_posts.to_excel('posts.xlsx', encoding='UTF-8')

print('SAVED')
