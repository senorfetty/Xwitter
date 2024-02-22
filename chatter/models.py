from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.

class Account(AbstractUser):
    groups= models.ManyToManyField(Group, related_name='accounts_set',blank=True)
    user_permissions= models.ManyToManyField(Permission, related_name='accounts_set', blank=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name= 'Account'
        verbose_name_plural= 'Accounts'