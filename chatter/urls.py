from . import views
from django.urls import path


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup', views.signup, name= 'signup'),
    path('login', views.log, name= 'login'),
    path('home', views.home, name= 'home'),
    path('logout_user', views.logout_user, name='logout'),
    path('passreset', views.passreset, name = 'passreset'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name= 'activate'),
]
