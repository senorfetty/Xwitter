from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import *
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
from .trends import get_trends
import os
from datetime import datetime
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import  LoginRequiredMixin, UserPassesTestMixin


load_dotenv()  

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, "You must be logged in to access this page.")
        return redirect('login')


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
    
    
def results(request):
    query= request.GET.get("query")
    search_list= Userprofile.objects.filter(Q(user__username__icontains=query))
    
        
    return render (request, "results.html", {'search_list':search_list}) 

    
def home(request):   
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')   
    
    tags= Tag.objects.all()

    profile_list = Account.objects.all()
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
   
    posts = Post.objects.all().order_by('-created_at') 
    username= Userprofile.objects.all()     
    trends= get_trends()
    
    if request.method == 'POST':   
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()      
            
            new_post.create_tag()          
            
            form = PostForm()       
            
    else:
        form = PostForm()     
        
        # user_profile = Userprofile.objects.get(user=request.user)
        # profile_picture_url = user_profile.picture.url if user_profile.picture else None
        
        
    return render(request, 'home.html',{'posts' : posts, 'form' :form, 'username':username,  'profile_list': profile_list,'not_count':not_count,'tags':tags,'trends':trends})

def explore(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')
    
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
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
 
    return render(request, 'explore.html', {'news' : filtered_news, 'trending_topics' : trending_topics, 'not_count' : not_count})

def replycomments(request,post_pk,pk):
    post= Post.objects.get(pk=post_pk)
    parent_comment= Comment.objects.get(pk=pk)
    
    if request.method == 'POST':
        form= CommentForm(request.POST)
        
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.author= request.user
            new_comment.post =  post
            new_comment.parent= parent_comment
            new_comment.save()
            
            new_comment.create_tag()
            
            form= CommentForm()
            
        notification = Notification.objects.create(notification_type=1,from_user=request.user,to_user=parent_comment.author,post=post)
            
    else:
        form= CommentForm()
        
    return redirect(reverse ('postdetail', kwargs={'pk':post_pk}))
        

def postcomments(request,pk):
    post= Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    trends= get_trends()
    tags= Tag.objects.all()
    profile_list = Account.objects.all()
    
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment= form.save(commit=False)
            comment.author=request.user
            comment.post= post            
            comment.save()
            
            form= CommentForm()   
            
        notification= Notification.objects.create(notification_type=1,from_user=request.user,to_user=post.author,post=post)         
            
    else:
        form=CommentForm()            
            
    return render(request, 'comments.html', {'post':post, 'form':form, 'comments':comments, 'trends':trends, 'tags':tags,'profile_list':profile_list,'not_count':not_count})

def nots(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')
    
    
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    
    return render(request, 'notification.html', {'notifications': notifications, 'not_count':not_count})

def postnotifications(request, notification_pk,post_pk):
    notification= Notification.objects.get(pk=notification_pk)
    post=Post.objects.get(pk=post_pk)
    
    
    notification.user_has_seen = True
    notification.save()
    
    return redirect ('postdetail' ,pk=post_pk) 

def follownotifications(request, notification_pk,profile_pk):
    notification= Notification.objects.get(pk=notification_pk)
    profile=Userprofile.objects.get(pk=profile_pk)
    
    
    notification.user_has_seen = True
    notification.save()
    
    return redirect ('profile',pk=profile_pk)  

def messagenotifications(request,notification_pk,thread_pk):
    notification = Notification.objects.get(pk=notification_pk)
    thread=Thread.objects.get(pk=thread_pk)
    
    notification.user_has_seen = True
    notification.save()
    
    return redirect ('thread', pk=thread_pk)

class PostEditView(CustomLoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Post
    fields= ['body']
    template_name= 'editpost.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('postdetail', kwargs={'pk': pk})
    
    def test_func(self):
        post= self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(CustomLoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    template_name= 'deletepost.html'
    success_url=  reverse_lazy('home')
    
    def test_func(self):
        post= self.get_object()
        return self.request.user == post.author
    
    
class CommentDeleteView(CustomLoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Comment
    template_name='deletecomment.html'
    
    def get_success_url(self):
        postpk = self.kwargs['post_pk']
        return reverse_lazy('postdetail', kwargs={'pk': postpk})

    def test_func(self):
        post= self.get_object()
        return self.request.user == post.author
    
    
def userProfile(request,pk):
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    profile = Userprofile.objects.get(pk=pk)
    user = profile.user
    posts= Post.objects.filter(author=user).order_by('-created_at')
    
    followers= profile.followers.all()
    
    
    
    if len(followers) == 0:
        is_following=False
    
    for follower in followers:
        if follower == request.user:
            is_following=True
            break
        else:
            is_following=False
    
    number_of_followers=  len(followers)
    
    context = {
        'profile':profile,
        'user':user,
        'posts':posts,
        'number_of_followers':number_of_followers,
        'is_following':is_following,        
        'not_count': not_count
    }
    
    return render(request, 'userprofile.html', context)

class EditProfileView(CustomLoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Userprofile
    form_class= EditProfileForm
    template_name="editprofile.html"
    
    def get_success_url(self):
        pk= self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk' : pk})
    
    def test_func(self):
        profile= self.get_object()
        return self.request.user == profile.user
    
def Followers(request,pk):
    profile= Userprofile.objects.get(pk=pk)
    profile.followers.add(request.user)
    
    notification= Notification.objects.create(notification_type=2,from_user=request.user,to_user=profile.user)
    
    return redirect('profile', pk=profile.pk) 

def Unfollowers(request,pk):
    profile= Userprofile.objects.get(pk=pk)
    profile.followers.remove(request.user)
    
    return redirect('profile', pk=profile.pk) 

def listfollowers(request,pk):
    profile = Userprofile.objects.get(pk=pk)    
    followers= profile.followers.all()
    
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    
    if len(followers) == 0:
        is_following=False
    
    for follower in followers:
        if follower == request.user:
            is_following=True
            break
        else:
            is_following=False
    
    
    context = {
        'followers':followers,
        'profile':profile,
        'is_following':is_following,
        'not_count':not_count      
    }
    
    return render(request, 'listoffollowers.html', context)

def likes(request,pk):
    post = Post.objects.get(pk=pk)
    
    is_dislike= False
    
    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
        break
    
    if is_dislike:
        post.dislikes.remove(request.user)
    
    is_like= False
    
    for like in post.likes.all():
        if like == request.user:
            is_like = True
        break
    
    if not is_like:
        post.likes.add(request.user)
        
        notification = Notification.objects.create(notification_type=0, from_user= request.user, to_user=post.author, post=post)
        
    if is_like:
        post.likes.remove(request.user)
        
    next= request.POST.get('next','/')
    return HttpResponseRedirect(next)
        
    
def dislikes(request,pk):
    post= Post.objects.get(pk=pk)
    
    is_like= False
    
    for like in post.likes.all():
        if like == request.user:
            is_like = True
        break
    
    if is_like:
        post.likes.remove(request.user)
    
    is_dislike= False
    
    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
        break
    
    if not is_dislike:
        post.dislikes.add(request.user)
        
    if is_dislike:
        post.dislikes.remove(request.user)
        
    next= request.POST.get('next','/')
    return HttpResponseRedirect(next)

def commentlikes(request,pk,post_pk):
    post= Post.objects.get(pk=post_pk)
    comment= Comment.objects.get(pk=pk)
    
    is_dislike= False
    
    for dislike in comment.dislikes.all():
        if dislike == request.user:
            dislike = True
        break
    
    if is_dislike:
        comment.dislikes.remove(request.user)
    
    is_like= False
    
    for like in comment.likes.all():
        if like == request.user:
            is_like = True
        break
    
    if not is_like:
        comment.likes.add(request.user)
    
        notification = Notification.objects.create(notification_type=0, from_user= request.user, to_user=comment.author, post=post)
        
    if is_like:
        comment.likes.remove(request.user)
        
    next= request.POST.get('next', '/')
    return  HttpResponseRedirect(next)

def commentdislikes(request,pk,post_pk):
    comment= Comment.objects.get(pk=pk)
    
    is_like= False
    
    for like in comment.likes.all():
        if like == request.user:
            is_like = True
        break
    
    if is_like:
        comment.likes.remove(request.user)
    
    is_dislike= False
    
    for dislike in comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
        break
    
    if not is_dislike:
        comment.dislikes.add(request.user)
        
    if is_dislike:
        comment.dislikes.remove(request.user)
        
    next= request.POST.get('next','/')
    return HttpResponseRedirect(next)

def childcommentlikes(request, post_pk, parent_pk, pk):
    child_comment = Comment.objects.get(pk=pk)
    
    is_dislike = False
    
    for dislike in child_comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
    
    if is_dislike:
        child_comment.dislikes.remove(request.user)
    
    is_like = False
    
    for like in child_comment.likes.all():
        if like == request.user:
            is_like = True
            break
    
    if not is_like:
        child_comment.likes.add(request.user)
        
        notification = Notification.objects.create(notification_type=0, from_user= request.user, to_user=child_comment.author)
    
    else:
        child_comment.likes.remove(request.user)
        
    next_url = request.POST.get('next', '/')
    return HttpResponseRedirect(next_url)

def childcommentdislikes(request, post_pk, parent_pk, pk):
    child_comment = Comment.objects.get(pk=pk)
    
    is_like = False
    
    for like in child_comment.likes.all():
        if like == request.user:
            is_like = True
            break
    
    if is_like:
        child_comment.likes.remove(request.user)
    
    is_dislike = False
    
    for dislike in child_comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
    
    if not is_dislike:
        child_comment.dislikes.add(request.user)
    else:
        child_comment.dislikes.remove(request.user)
        
    next_url = request.POST.get('next', '/')
    return HttpResponseRedirect(next_url)

def msg(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')
    
    profile= Userprofile.objects.all().filter(name=request.user)
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    

    threads= Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))    
   
    
    return render(request, 'messages.html',{'threads':threads,'profile':profile, 'not_count':not_count})

def createthread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        
        username= request.POST.get('username')       
        
        try:
            receiver = Account.objects.get(username=username)
            if Thread.objects.filter(user=request.user,receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user,receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif  Thread.objects.filter(user=receiver,receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver,receiver=request.user)[0]
                return redirect ('thread', pk=thread.pk)
            
            if form.is_valid():
                thread= Thread(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                
                return redirect ('thread', pk=thread.pk)
        
        except:
            messages.error(request,"Username not found")
            return redirect ('createthread')
            
    else:
        form= ThreadForm()
        notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
        not_count= notifications.count()    
        
    return render(request, 'thread.html', {'form':form,'not_count':not_count})
    
    
def inbox(request,pk):
    form = MessageForm()
    thread= Thread.objects.get(pk=pk)
    message_list= Message.objects.filter(thread__pk__contains=pk)
    
    notifications= Notification.objects.filter(to_user=request.user,user_has_seen=False).exclude(from_user=request.user)
    not_count= notifications.count()    
    
    context = {
        'message_list' : message_list,
        'thread' : thread,
        'form' : form,
        'not_count' : not_count
    }
    
    return render (request,'inbox.html',context)

def createmessage(request,pk):
    form= MessageForm(request.POST,request.FILES)
    thread=Thread.objects.get(pk=pk)
    
    if thread.receiver == request.user:
        receiver= thread.user
    else:
        receiver= thread.receiver
        
    if form.is_valid():
        message= form.save(commit=False)
        message.thread=thread
        message.sender_user=request.user
        message.receiver_user=receiver
        
        message.save()
    
    notification= Notification.objects.create(notification_type=3,to_user=receiver,from_user=request.user,thread=thread)
    
    return redirect('thread', pk=pk)

class MessageDelete(DeleteView):
    model=Message
    success_url= reverse_lazy('inbox')
    
