from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import  receiver

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
    likes= models.ManyToManyField(Account, blank=True, related_name='likes')
    dislikes= models.ManyToManyField(Account, blank=True, related_name='dislikes')
   
    class Meta:
        verbose_name= 'Post'
        verbose_name_plural= 'Posts'
        

        
class Comment(models.Model):
    comment= models.TextField()
    created_at= models.DateTimeField(default=timezone.now, editable=False)
    author= models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    

class Userprofile(models.Model):
    user= models.OneToOneField(Account,primary_key=True,verbose_name='user',related_name='profile',on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True, null=True)
    bio= models.TextField(max_length=200,blank=True,null=True)
    location= models.CharField(max_length=50, null=True,blank=True)
    birth_date=models.DateField(null=True,blank=True)
    picture= models.ImageField(upload_to='uploads/profile_pictures',default='uploads/profile_pictures/default.jpg',blank=True,null=True)
    followers= models.ManyToManyField(Account, blank=True, related_name='followers')

@receiver(post_save, sender=Account)
def  create_userprofile(sender, instance,created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)
        
@receiver(post_save, sender=Account)
def  save_userprofile(sender, instance, **kwargs):
    instance.profile.save()