# import tweepy
# import os
# from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# load_dotenv()

# def twitterapi():
#     consumer_key= os.getenv('twitterapikey')
#     consumer_secret= os.getenv('twitterapisecret')
#     access_token= os.getenv('accessToken')
#     access_token_secret= os.getenv('accessTokenSecret')
    
#     auth=tweepy.OAuth1UserHandler(consumer_key,consumer_secret,access_token,access_token_secret)
#     api=tweepy.API(auth)
#     return api

# def trending(api,woeid=1):
#     api= twitterapi()
#     trends=api.get_place_trends(woeid)
#     trending_topics=[]
#     for trend in trends[0]['trends']:
#         trending_topics.append(trend['name'])
        
#     return trending_topics

