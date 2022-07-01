from django.urls import path, include
from djoser import views as djoser_views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # user views
    path('<int:pk>', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # token views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # djoser views
    path('', djoser_views.UserViewSet.as_view({'post': 'create'}),
         name="register"),
    path("resend-activation/", djoser_views.UserViewSet.as_view({"post": "resend_activation"}),
         name="resend_activation"),
    path("activation/<str:uid>/<str:token>/", djoser_views.UserViewSet.as_view({"post": "activate"}), name="activate"),
    path("reset-password/", djoser_views.UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset-password-confirm/<str:uid>/<str:token>/",
         djoser_views.UserViewSet.as_view({"post": "reset_password_confirm"}),
         name="reset_password_confirm"),
]

# user registration: POST http://127.0.0.1:8000/api/v1/users/
# user login:        POST http://127.0.0.1:8000/api/v1/users/token/
# refresh token:     POST http://127.0.0.1:8000/api/v1/users/token/refresh/
