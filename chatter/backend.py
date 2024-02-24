from django.contrib.auth.backends import BaseBackend
from .models import Account

class AuthBackend(BaseBackend):
    def authenticate(self, request, username= None, password= None, **kwargs):
        try:    
            user= Account.objects.get(username=username)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            pass
            
        
    def  get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id) 
        
        except Account.DoesNotExist:
            return None
        