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
    path('events/attend/<int:event_id>/', views.attend_event, name='attend_event'),
    path('events/cancel/<int:event_id>/', views.cancel_event, name='cancel_event'),
    path('view_profile', views.view_profile, name='view_profile'),
]