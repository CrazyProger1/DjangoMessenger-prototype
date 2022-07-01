from django.urls import path, include

urlpatterns = [
    path('token/', include('users.auth_urls'))
]
