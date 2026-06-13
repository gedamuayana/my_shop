from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from .views import signup_view
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.submit_deposit, name='deposit'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup_view, name='signup'),
]
from django.urls import path
from .views import signup_view  # ይህንን ከላይ መጨመር እንዳትረሳ

