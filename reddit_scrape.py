import requests
import pandas as pd
import copy
import os.path
import time
from uuid import uuid4 as uuid
from bs4 import BeautifulSoup
import numpy as np

from scrapers import post_scrape, metrics_scrape, user_scrape, comments_scrape

if __name__ == "__main__":
    start_time = time.time()
    users = {}
    for i in range(1, 2):  # number of subreddits to scrape
        df = pd.DataFrame()
        scraped_data = []
        post_id = None

        url = "http://www.reddit.com/r/random/"
        html = requests.get(url, headers={"User-agent": str(uuid())})
        soup = BeautifulSoup(html.text, 'lxml')

        subreddit, subs, subreddit_rank = metrics_scrape(copy.copy(soup))

        errors = 0

        print(i, subreddit)

        for j in range(1, 41):  # number of pages for each subreddit

            if not post_id:
                pass
            else:
                url = "http://www.reddit.com/r/{}/?count=25&after={}".format(subreddit, post_id)
                html = requests.get(url, headers={"User-agent": str(uuid())})
                soup = BeautifulSoup(html.text, 'lxml')

            for posts in soup.findAll(name='div', attrs={'id': 'siteTable'}):
                for post in soup.findAll(name='div', attrs={'data-context': 'listing'}):

                    try:
                        data = post_scrape(copy.copy(post))

                        post_id = data['post_id']

                        data['subscriptions'] = subs
                        data['subreddit_rank'] = subreddit_rank

                        # author = data['author']
                        # if author not in users.keys():
                        #     users[author] = {}
                        #     users[author]['karma'], users[author]['comment_karma'] = user_scrape(author)

                        # data['karma'] = users[author]['karma']
                        # data['comment_karma'] = users[author]['comment_karma']

                        data['karma'] = np.NaN
                        data['comment_karma'] = np.NaN

                        scraped_data.append(data)

                        print("\t- page: {}, subreddit: {}, author: {}, title: {}".format(j,
                                                                                          data['subreddit'],
                                                                                          data['author'],
                                                                                          data['title']))
                    except:
                        errors += 1
                        if errors == 5:
                            break
                        else:
                            continue

        df = df.append(scraped_data)

        if not os.path.isfile('raw_data/scraped_data.csv'):
            print("NEW FILE")
            df.to_csv('raw_data/scraped_data.csv', index=False)
        else:
            df.to_csv('raw_data/scraped_data.csv', index=False, mode='a', header=False)

    print("\nELAPSED TIME: {:.2f} Minutes".format((time.time() - start_time)/60))
