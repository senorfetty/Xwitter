from . import views
from .views import PostEditView, PostDeleteView, CommentDeleteView, EditProfileView
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup', views.signup, name= 'signup'),
    path('login', views.log, name= 'login'),
    path('home/', views.home, name= 'home'),
    path('searchresults/', views.results, name= 'results'),    
    path('followers_list/<int:pk>/', views.listfollowers, name='lof'),
    path('home/post/<int:post_pk>/comment/<int:pk>/like', views.commentlike, name= 'commentlike'),
    path('home/post/<int:post_pk>/comment/<int:pk>/dislike', views.commentdislike, name= 'commentdislike'),
    # path('dislike/<int:pk>/', views.dislike_post_ajax, name='dislike_post_ajax'),
    path('like/<int:pk>', views.likes, name= 'likes'),
    path('dislike/<int:pk>', views.dislikes, name= 'dislikes'),
    path('profile/<int:pk>/', views.userProfile, name= 'profile'),
    path('profile/<int:pk>/followers/add', views.Followers, name= 'addfollower'),
    path('profile/<int:pk>/followers/remove', views.Unfollowers, name= 'removefollower'),
    path('profile/edit_profile/<int:pk>/', EditProfileView.as_view(), name= 'editprofile'),
    path('home/post/<int:pk>/', views.postcomments, name= 'postdetail'),
    path('home/post/edit/<int:pk>/', PostEditView.as_view() , name= 'editpost'),
    path('home/post/delete/<int:pk>/', PostDeleteView.as_view() , name= 'deletepost'),
    path('home/post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view() , name= 'deletecomment'),
    path('email_confirmation', views.confemail, name='conf'),
    path('invalid_link', views.inv, name='inval'),
    path('explore', views.explore, name= 'explore'),
    path('notifications', views.nots, name= 'notifications'),
    path('messages', views.msg, name= 'messages'),
    path('logout_user', views.logout_user, name='logout'),    
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="passreset.html",html_email_template_name='passresetemail.html',),name="password_reset"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="passresetdone.html"),name="password_reset_done"),
    path('reset/<slug:uidb64>/<slug:token>',auth_views.PasswordResetConfirmView.as_view(template_name="passresetconfirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="passresetcomplete.html"),name="password_reset_complete"),
] 


    
