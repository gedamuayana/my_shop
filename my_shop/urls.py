from django.contrib import admin
from django.urls import path
from core import views # ከ . ፋንታ core ብለው ያርሙት

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    # የቀሩትን መስመሮች እንዳለ ይተዉዋቸው...
]