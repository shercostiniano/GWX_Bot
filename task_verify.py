import time

from tweepy import api


def facebook_verify():
    import json
    import requests

    token = " "
    fan_count = "https://graph.facebook.com/v3.2/293570938130414?fields=fan_count&access_token=" + token
    check_fans = requests.get(fan_count)
    json_fans = json.loads(check_fans.text)

    return json_fans['fan_count']


def twitter_verify():
    import tweepy

    auth = tweepy.OAuthHandler('', '')
    auth.set_access_token('',
                          '')
    api = tweepy.API(auth)

    ids = []
    for page in tweepy.Cursor(api.followers_ids).pages():
        ids.extend(page)

    return len(ids)

def instagram_verify():
    pass


def youtube_verify():
    pass
