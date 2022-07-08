from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('', ChatViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('members/my/', MyChatMembersListAPIView.as_view()),
    path('<int:chat_pk>/members/', ChatMemberViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:chat_pk>/members/<int:pk>', ChatMemberViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}))
]
