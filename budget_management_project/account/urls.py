from django.urls import path
from .views import RegisterView

app_name = "account"

urlpatterns = [
    path('account', RegisterView.as_view(), name='account'),
]
