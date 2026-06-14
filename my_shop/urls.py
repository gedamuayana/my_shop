from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # ባዶ ዩአርኤል ሲገባ በቀጥታ ወደ ትክክለኛው የ en-us ቋንቋ ራውተር ይመራል
    path('', RedirectView.as_view(url='/en-us/', permanent=False)),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')), # በቀጥታ ወደ core/urls.py ይመራል
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)