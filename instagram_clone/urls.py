from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('api/', include('api.urls')),
    path('shop/', include('shop.urls')),
    path('chat/', include('chat.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)