from django.urls import path
from rest_framework import routers

from .views import list_songs, submit_song_rating

routers =  routers.DefaultRouter()

urlpatterns = [
    path('api/v1/songs/', list_songs),
    path('api/v1/rate_song/', submit_song_rating),
]

urlpatterns += routers.urls