from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.submit_deposit, name='submit_deposit'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('signup/', views.signup_view, name='signup'),
]