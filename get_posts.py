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
"""
# TODO: create a generic method to request Instagram data from different APIs, not only the Dialogfeed's one.

import time
import random
import os
import csv
from datetime import datetime

import requests
import pandas as pd

# Read the API key from environment variable
api_key = os.environ['instagram_api_key']

# get current date (used to calculate running elapsed time)
now = datetime.now()
now_str = now.strftime("%d_%m_%Y-%H_%M_%S")

# Retrieve data (paginated calls are done consecutively to the API until no more data are returned)
rows_list = list()
last_uid = ""
while last_uid is not None:
    print(f"NEXT PAGINATION. With last uid: {last_uid}")
    if last_uid != "":
        pagination_parameter = last_uid
    else:
        pagination_parameter = None
    payload = {'api_key': api_key, 'max': '400', 'max_id': pagination_parameter}
    r = requests.get(f'https://app.dialogfeed.com/en/snippet/mallorca.json', params=payload)
    print("calling to ", r.url)
    result = r.json()['news_feed']
    last_uid = result['posts']['post'][0]['uid']

    for post in result['posts']['post']:
        try:
            if post['source']['source_url'] is not None:
                if "https://www.instagram.com/p/" in post['source']['source_url']:
                    print('Getting data more from', post['source']['source_url'])
                    print(post['created_at_std'])
                    print(post['uid'])
                    print('Content body', post['content']["content_body"].replace('\n', ' . '))
                    print('Language:', post['language'])
                    print("\n______________________\n")
                else:
                    print(post['source']['source_url'])
                    print(post['uid'])
                    print("\n______________________\n")

        except Exception as e:
            print(e)
            # time.sleep(random.randint(5, 21))
            print("\n______________________\n")
    time.sleep(random.randint(3, 10))

# Save retrieved data to CSV
filename = f'paginated_out/posts_dialog_feed_{now_str}_.csv'
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
