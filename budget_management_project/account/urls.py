from django.urls import path
from .views import RegisterView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "account"

urlpatterns = [
    path('account', RegisterView.as_view(), name='account'),
    path('account/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
]
