# import tweepy
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

def get_trends():    
    api_key= os.getenv('newsapikey')
    url= f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
   
    response= requests.get(url)
    data=response.json()  
    
    news= data.get('articles')    
    
    filtered_news= []   
    
    for article in news:
        if article.get('content') and '[Removed]'  not in article['title'] :
            published_time= datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            article['publishedAt']= published_time.strftime( "%d/%B/%Y %H:%M ") 
            filtered_news.append(article) 
        
    trending_topics = [article['title'][:20] for article in news if article.get('content') and '[Removed]' not in article['title']]
    return trending_topics