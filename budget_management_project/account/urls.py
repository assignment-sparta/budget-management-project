from django.urls import path
from .views import RegisterView, LoginView

app_name = "account"

urlpatterns = [
    path('account', RegisterView.as_view(), name='account'),
    path('account/login', LoginView.as_view(), name='login'),
    
]
