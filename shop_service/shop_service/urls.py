from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title='Shop Service APIs',
        default_version='v1',
        description='API documentation for Shop Service',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('shops.urls_v1')),
]

urlpatterns += (
     # Swagger & Redoc documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
)

if settings.DEBUG:
    if getattr(settings, 'MEDIA_URL', None):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if getattr(settings, 'STATIC_URL', None):
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)