from django.urls import path, include
from djoser.views import UserViewSet
from .views import *

urlpatterns = [
    path('token/', include('users.token_urls')),

    path('', UserViewSet.as_view({'post': 'create'}), name="register"),
    path("resend-activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend_activation"),
    path("activation/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "activate"}), name="activate"),
    path("reset-password/", UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset-password-confirm/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "reset_password_confirm"}),
         name="reset_password_confirm"),
]

# user registration: POST http://127.0.0.1:8000/api/v1/users/
# user login:        POST http://127.0.0.1:8000/api/v1/users/token/
# refresh tokens:    POST http://127.0.0.1:8000/api/v1/users/token/refresh/
