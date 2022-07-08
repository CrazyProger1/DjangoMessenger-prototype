from django.urls import path, include

from rest_framework import routers

from .views import *

urlpatterns = [
    path('', MessageListAPIView.as_view())
]
