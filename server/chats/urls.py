from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('', ChatViewSet)

urlpatterns = router.urls
