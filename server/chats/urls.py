from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ChatViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', ChatViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
        'delete': 'destroy'
    }))
]
