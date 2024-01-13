from django.urls import path
from . import views

app_name = 'agecode'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_user, name='register'),
    path('events/', views.user_events, name='events'),
    path('events/<int:pk>', views.event_details, name='details'),
    path('add_event', views.add_event, name='add_event'),
]