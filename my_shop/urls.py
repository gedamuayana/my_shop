from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views  # ሆም ፔጅ ቪው እንዲነበብ

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # ዋናው መግቢያ ገጽ (Home page) በቀጥታ እንዲነበብ
                  path('', views.home_view, name='home'),
                  path('', include('core.urls')),

                  # የይለፍ ቃል መቀየሪያ ሊንኮች (Forgot Password)
                  path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
                       name='password_reset'),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                       name='password_reset_confirm'),
                  path('reset/done/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                       name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)