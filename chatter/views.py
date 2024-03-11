from django.shortcuts import render,redirect
from .forms import RegForm, PostForm
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models.query_utils import  Q
from django.contrib.auth.tokens import default_token_generator
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from .models import Account, Post
from dotenv import load_dotenv
import requests
import os
from datetime import datetime
from pytrends.request import TrendReq



load_dotenv()  

def welcome(request):
    return render(request, 'welcome.html')

def signup(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        
        if form.is_valid():
            user= form.save(commit=False)
            user.is_active= False
            user.save()
        
            current_site= get_current_site(request)
            mail_subject= 'Activation Link has been sent to you'

            message= render_to_string('email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)            
            })
            
            data= form.cleaned_data.get('email')
            send_mail(mail_subject,message,'chatterchuckles@gmail.com', [data],fail_silently=False)
            return redirect('conf')
        
    else:
        form = RegForm()
        
    return render(request, 'signup.html', {'form': form})

def confemail(request):
    return render(request, 'conf.html')

def inv(request):
    return render(request, 'invalid.html')
    
def log(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        user= authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,'Username or Password is incorrect')
            return redirect('login')
    
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active= True
        user.save()
        return redirect('login')
    else:
        return redirect('inval')
    
    
def home(request):   
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':        
        form = PostForm(request.POST)
        
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()               
            
    else:
        form = PostForm()           
        
    return render(request, 'home.html',{'posts' : posts, 'form' :form})

def explore(request):
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
 
    return render(request, 'explore.html', {'news' : filtered_news, 'trending_topics' : trending_topics})


def msg(request):
    return render(request, 'messages.html')

def nots(request):
    return render(request, 'notification.html')

