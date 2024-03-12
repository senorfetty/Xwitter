from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils import timezone

# Create your models here.

class Account(AbstractUser):
    groups= models.ManyToManyField(Group, related_name='accounts_set',blank=True)
    user_permissions= models.ManyToManyField(Permission, related_name='accounts_set', blank=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name= 'Account'
        verbose_name_plural= 'Accounts'
        
class Post(models.Model):
    body= models.TextField()
    created_at= models.DateTimeField(default=timezone.now, editable=False)
    author= models.ForeignKey(Account, on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name= 'Post'
        verbose_name_plural= 'Posts'
        
class Comment(models.Model):
    comment= models.TextField()
    created_at= models.DateTimeField(default=timezone.now, editable=False)
    author= models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)