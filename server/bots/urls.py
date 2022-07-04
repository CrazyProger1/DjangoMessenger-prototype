from django.urls import path, include
from .views import *

urlpatterns = [
    path('', BotViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', BotViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}))
]
