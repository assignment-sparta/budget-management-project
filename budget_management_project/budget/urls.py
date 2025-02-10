from django.urls import path
from . import views

app_name = "budget"

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category-list'),
]
