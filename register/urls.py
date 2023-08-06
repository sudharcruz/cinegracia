from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset/complete/',custom.as_view(),name='password_reset_complete'),
    
]
