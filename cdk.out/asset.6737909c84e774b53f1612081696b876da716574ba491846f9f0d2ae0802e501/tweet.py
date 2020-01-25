import boto3
from twitter import OAuth, Twitter
import requests
from bs4 import BeautifulSoup
import random


def tweet(event, context):
    ####################### WEB SCRAPING ######################################

    r = requests.get('https://greengocloud.com/archives/')

    p = []

    soup = BeautifulSoup(r.text, 'html.parser')

    posts = soup.find_all(class_='archive-article-title')

    for post in posts:
        #print(post)
        title = post.get_text()
        #print(title)
        link = post.get('href')
        tl = title + ' #aws #greengocloud ' + 'https://greengocloud.com' + link
        p.append(tl)

    blog = random.choice(p)

    print(blog)

    ##################### TWITTER ############################################
    CONSUMER_KEY_PARAM_NAME = '/{}/consumer_key'.format('tsgt_green')
    CONSUMER_SECRET_PARAM_NAME = '/{}/consumer_secret'.format('tsgt_green')
    OAUTH_TOKEN_PARAM_NAME = '/{}/access_token'.format('tsgt_green')
    OAUTH_SECRET_PARAM_NAME = '/{}/access_token_secret'.format('tsgt_green')

    SSM = boto3.client('ssm')

    param_names=[
        CONSUMER_KEY_PARAM_NAME,
        CONSUMER_SECRET_PARAM_NAME,
        OAUTH_TOKEN_PARAM_NAME,
        OAUTH_SECRET_PARAM_NAME
    ]

    response = SSM.get_parameters(
        Names=param_names,
        WithDecryption=True
    )

    param_lookup = {param['Name']: param['Value'] for param in response['Parameters']}

    oauth_token=param_lookup[OAUTH_TOKEN_PARAM_NAME]
    oauth_secret=param_lookup[OAUTH_SECRET_PARAM_NAME]

    t = Twitter(
        auth=OAuth(
            oauth_token,
            oauth_secret,
            consumer_key=param_lookup[CONSUMER_KEY_PARAM_NAME],
            consumer_secret=param_lookup[CONSUMER_SECRET_PARAM_NAME],
        )
    )

    t.statuses.update(status=blog)
