from django.urls import path
from .views import RegisterView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "account"

urlpatterns = [
    path('account', RegisterView.as_view(), name='account'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
]
