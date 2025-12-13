from django.urls import path
from rest_framework import routers

from .views import list_songs

routers =  routers.DefaultRouter()

urlpatterns = [
    path('api/v1/songs/', list_songs),
]

urlpatterns += routers.urls