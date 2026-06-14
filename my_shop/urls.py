from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # ባዶ ዩአርኤል ሲገባ በቀጥታ ወደ እንግሊዝኛ ቋንቋ ራውተር (en) ይመራል
    path('', lambda request: redirect('/en/')),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')), # የቋንቋ ምርጫ የሚደረግባቸው ገጾች እዚህ ይካተታሉ
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)