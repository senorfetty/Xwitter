from django import forms
from django.contrib.auth.forms import UserCreationForm
from. models import Account, Post


class RegForm(UserCreationForm):
    first_name= forms.CharField(max_length = 30,required=True, help_text='Required')
    last_name= forms.CharField(max_length = 40, required = True, help_text='Required')
    username= forms.CharField(max_length=30, required=True)
    email= forms.EmailField(help_text="Please enter a valid email address.",required=True)
    date_of_birth= forms.DateField(help_text="Format: DD-MM-YYYY", widget=forms.DateInput(attrs= {'type':'date', 'min' : '01-01-1924', 'max' : '31-12-2014','id':'datepicker'}))
    
    class Meta:
        model = Account
        fields= ('first_name', 'last_name', 'username', 'email', 'date_of_birth', 'password1', 'password2')
    
class PostForm(forms.ModelForm):
    body= forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5,'placeholder': 'What\'s on Your Mind Today?'}))
    
    class Meta:
        model = Post
        fields= ['body']
    