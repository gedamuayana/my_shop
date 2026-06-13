from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import signup_view
urlpatterns = [
    path('admin/', admin.site.urls),
path('signup/', signup_view, name='signup'),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)