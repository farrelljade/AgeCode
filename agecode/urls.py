from django.urls import path
from . import views

app_name = 'agecode'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]