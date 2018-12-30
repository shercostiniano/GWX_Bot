import json
import requests


def facebook_verify():
    token = " "
    link = "https://graph.facebook.com/v3.2/293570938130414?fields=fan_count&access_token=" + token
    request_link = requests.get(link)
    fan_count = json.loads(request_link.text)['fan_count']

    return fan_count


def twitter_verify():
    import tweepy

    auth = tweepy.OAuthHandler('', '')      #CONSUMER
    auth.set_access_token('',               #KEY
                          '')
    api = tweepy.API(auth)

    follower_count = []
    for page in tweepy.Cursor(api.followers_ids).pages():
        follower_count.extend(page)

    return len(follower_count)


def instagram_verify():
    name = ""
    link = 'https://www.instagram.com/web/search/topsearch/?query={' + name + ')'
    request_link = requests.get(link)
    follower_count = json.loads(request_link.text)['users'][0]['user']['follower_count']

    return follower_count


def youtube_verify():
    channel_id = ""
    token = ""
    link = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + token
    request_link = requests.get(link)
    subscriber_count = json.loads(request_link.text)["items"][0]["statistics"]["subscriberCount"]

    return subscriber_count
