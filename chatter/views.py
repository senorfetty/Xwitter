from django.shortcuts import render,redirect
from .forms import RegForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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