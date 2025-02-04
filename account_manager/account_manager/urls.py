from django.contrib import admin
from django.urls import path

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularYAMLAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # swagger
    path("swagger.json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("swagger.yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui", ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc", ),
]
