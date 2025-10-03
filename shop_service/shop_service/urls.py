from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from shop_service.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)