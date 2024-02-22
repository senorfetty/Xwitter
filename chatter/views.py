from django.shortcuts import render,redirect
from .forms import RegForm

# Create your views here

def welcome(request):
    return render(request, 'welcome.html')

def signup(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect ('login')
        
    else:
        form = RegForm()
    return render(request, 'signup.html', {'form': form})

def log(request):
    return render(request, 'login.html')