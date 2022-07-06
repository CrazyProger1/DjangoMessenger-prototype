from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('', ChatViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('', ChatViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('<int:pk>/', ChatViewSet.as_view({
#         'get': 'retrieve',
#         'patch': 'partial_update',
#         'put': 'update',
#         'delete': 'destroy'
#     }))
# ]