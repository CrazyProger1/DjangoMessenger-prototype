from django.urls import path, include
from .views import *

urlpatterns = [
    path('', BotListCreateAPIView.as_view()),
    path('<int:pk>/', BotRetrieveUpdateDestroyAPIView.as_view()),
    path('me/', BotRetrieveAPIView.as_view()),
]
