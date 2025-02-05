from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
]



swagger_urlpatterns = [
    path("swagger.json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("swagger.yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += swagger_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
