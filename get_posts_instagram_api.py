#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get Instagram posts using the Dialogfeed API (trial version).
API calls are paginated based on the value of last_uid.
If not last_uid is provided in the last call the extraction stops.
Api key is provided as environment variable. This way we protect sensitive information.
The data retrieved for each post are:
* creation date
* unique identifier in Instagram (uid). The post URL can be inferred with it.
* content (text)
* text language
Data are saved in CSV files
Limitations, permissions and characteristics of the endpoint:
https://developers.facebook.com/docs/instagram-api/reference/hashtag/recent-media/?locale=es_ES#returnable-fields

https://developers.facebook.com/docs/graph-api/overview/rate-limiting
"""
# TODO: create a generic method to request Instagram data from different APIs, not only the Dialogfeed's one.

import time
# import random
import os
import csv
from datetime import datetime

import requests
import pandas as pd

# Read the API key from environment variable
api_key = os.environ['instagram_access_token']

# get current date (used to calculate running elapsed time)
now = datetime.now()
now_str = now.strftime("%d_%m_%Y-%H_%M_%S")

# Retrieve data (paginated calls are done consecutively to the API until no more data are returned)
rows_list = list()
next_page = f"https://graph.facebook.com/v6.0/17841563143080743/recent_media?fields=caption,like_count,comments_count,media_type,permalink&user_id=17841404801388105&access_token={api_key}&limit=50"

while next_page is not None:
    print(f"PROCESSING PAGE:  {next_page}")
    # payload = {'api_key': api_key, 'max': '400', 'max_id': pagination_parameter}
    r = requests.get(next_page)
    print("calling to ", r.url)
    result = r.json()

    # Control pagination
    if 'paging' in result:
        if 'next' in result['paging']:
            next_page = result['paging']['next']
        else:
            next_page = None
    else:
        next_page = None

    # Get relevant data
    if 'data' in result:
        if len(result['data']) > 0:
            for post in result['data']:
                try:
                    print('Link', post['permalink'])
                    print('Caption', post['caption'].replace('\n', ' . '))
                    print('Comments count', post['comments_count'])
                    print('Media Type:', post['media_type'])
                    print('ID:', post['id'])
                    # print('IG_ID:', post['ig_id'])
                    # print('Timestamp:', post['timestamp'])
                    # print('Username:', post['username'])
                    print("\n______________________\n")
                    # Add brand to post
                    post['brand'] = 'mallorca'

                    # control absence of non mandatory fields
                    if 'caption' not in post:
                        post['caption'] = ''
                    if 'comments_count' not in post:
                        post['comments_count'] = 0
                    if 'media_type' not in post:
                        post['media_type'] = 'UNKNOWN'

                    # remove breaklines in caption.
                    post['caption'] = post['caption'].replace('\n', '')

                    # Append extracted posts to the CSV rows_list
                    rows_list.append(post)
                except Exception as e:
                    print(e)
                    # time.sleep(random.randint(5, 21))
                    print("\n______________________\n")
        else:
            next_page = None
    # time.sleep(random.randint(3, 10))
    # Sleep to avoid exhausting the rate limit
    # Allowed Calls within one hour = 200 * Number of Users
    # https://developers.facebook.com/docs/graph-api/overview/rate-limiting
    time.sleep(20)

# Save retrieved data to CSV
filename = f'paginated_out/posts_instagram_{now_str}.csv'
dir_name = os.path.dirname(filename)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

data_df = pd.DataFrame(rows_list)
data_df.to_csv(filename, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)

# Report running time
lapse = datetime.now() - now
print(now)
print(datetime.now())
print("The extraction Took nearly  ", int(round(lapse.total_seconds()/60, 0)), ' minute(s)')
