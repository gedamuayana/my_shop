from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language  # የቋንቋ መቀየሪያውን ቪው በቀጥታ እናስገባዋለን

urlpatterns = [
    path('admin/', admin.site.urls),
    # ራውተሩን በቀጥታ ከስሙ (name='set_language') ጋር እናገናኘዋለን
    path('i18n/', set_language, name='set_language'),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)