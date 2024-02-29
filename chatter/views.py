from django.shortcuts import render,redirect
from .forms import RegForm
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.db.models.query_utils import  Q
from django.contrib.auth.tokens import default_token_generator
from  .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from .models import Account

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
            return HttpResponse('Please confirm Email and complete registration')
        
    else:
        form = RegForm()
        
    return render(request, 'signup.html', {'form': form})

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
        return HttpResponse('Activation Link Invalid')
    

def home(request):
    return render(request, 'home.html')

def explore(request):
    return render(request, 'explore.html')

def msg(request):
    return render(request, 'messages.html')

def nots(request):
    return render(request, 'notification.html')
    
