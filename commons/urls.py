from rest_framework import routers
from .views import  health_check
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/health_check', health_check),
]

