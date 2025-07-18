from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('player.urls',namespace='music player')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
