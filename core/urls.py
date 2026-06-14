from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.submit_deposit, name='deposit'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),

    # የቋንቋ መቀየሪያ ዱካ (URL) እዚህ ይጨመራል
    path('set-language/', views.set_language_view, name='set_language'),
]