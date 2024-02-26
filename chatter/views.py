from django.shortcuts import render,redirect
from .forms import RegForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from .models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.db.models.query_utils import  Q
from django.contrib.auth.tokens import default_token_generator
from  .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site


def welcome(request):
    return render(request, 'welcome.html')

def signup(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
        
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

def home(request):
    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    return redirect('login')


def passreset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data= form.cleaned_data['email']
            users= Account.objects.filter(Q(email=data))
            
            if users.exists():
                for user in users:
                    subject= 'Password Reset'
                    
                    message = render_to_string('passresetemail.html', {
                        'name': user.first_name,
                        'email': user.email,
                        'domain': get_current_site(request).domain,
                        'site_name':'Chatter',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                    })                       
                    
                    try:
                        send_mail(subject,message,'chatterchuckles@gmail.com', [user.email],fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse ('Invalid Header Found')
                    return redirect('passreset/done')
    
    form= PasswordResetForm()
    return render(request, 'passreset.html', {'form': form})

def activate(uidb64,token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except {TypeError, ValueError, OverflowError, Account.DoesNotExist}:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    
    else:
        return HttpResponse('Activation Link Invalid')
        