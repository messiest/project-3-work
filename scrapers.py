import datetime
import requests
from bs4 import BeautifulSoup
from uuid import uuid4 as uuid
import numpy as np
from selenium import webdriver

def post_scrape(post):

    try:
        post_id = post['data-fullname']
    except:
        post_id = np.NaN

    try:
        t_stamp = post['data-timestamp']
    except:
        t_stamp = np.NaN

    try:
        content = post['data-url']
    except:
        content = np.NaN

    try:
        permalink = post['data-permalink']
    except:
        permalink = None

    try:
        title = post.find('p', {'class': 'title'}).text
    except:
        title = np.NaN

    try:
        score = int(post.find('div', {'class': 'score unvoted'})['title'])
    except:
        score = np.NaN

    try:
        author = post.find('a', {'class': 'author'}).text
    except:
        author = np.NaN

    try:
        subreddit = "r/{}".format(post['data-subreddit'])
    except:
        subreddit = np.NaN

    try:
        comments = int(post['data-comments-count'])
    except:
        comments = np.NaN

    try:
        crossposts = post['data-num-crossposts']

    except:
        crossposts = np.NaN

    data = {'scrape_time': datetime.datetime.now().timestamp(),
            'post_time': t_stamp,
            'post_id': post_id,
            'title': title,
            'score': score,
            'comments': comments,
            'author': author,
            'subreddit': subreddit,
            'crossposts': crossposts,
            'link': permalink,
            'content': content}

    return data


def metrics_scrape(html):
    try:
        pagename = html.find(name='span', attrs={'class': 'hover pagename redditname'})
        subreddit = pagename.find(name='a').text

        metrics_url = "https://www.redditmetrics.com/r/{}".format(subreddit)
        metrics_html = requests.get(metrics_url)
        soup_2 = BeautifulSoup(metrics_html.text, 'lxml')
        metrics = [int(i.text.replace(',', '')) for i in soup_2.findAll('h2')]
        subscriptions = metrics[0]
        subreddit_rank = metrics[1]

        return subreddit, subscriptions, subreddit_rank
    except:
        return np.NaN, np.NaN, np.NaN

def user_scrape(user_name):

    try:

        url = "https://www.reddit.com/user/{}".format(user_name)

        html = requests.get(url, headers={"User-agent": str(uuid())})
        user_page = BeautifulSoup(html.text, "lxml")

        karma = int(user_page.find('span', attrs={'class': 'karma'}).text.replace(',', ''))
        comment_karma = int(user_page.find('span', attrs={'class': 'karma comment-karma'}).text.replace(',', ''))

        return karma, comment_karma

    except:

        return np.NaN, np.NaN


def comments_scrape(post):
    try:
        comments_url = "https://www.reddit.com{}".format(post['data-permalink'])

        driver = webdriver.Chrome(executable_path="/Users/monolith/Downloads/chromedriver")
        driver.get(comments_url)

        comments_html = driver.page_source
        soup = BeautifulSoup(comments_html.text, 'lxml')

        text_data = []
        for comment in soup.findAll(name='div', attrs={'data-type': 'comment'}):
            for texts in comment.findAll(name='div', attrs={'class': 'md'}):
                for text in texts.findAll(name='p'):
                    text_data.append(text.text)

        driver.close()
        return " ".join(text_data)
    except:
        return np.NaN
