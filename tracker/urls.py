from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_ip, name='track_ip'),
]
