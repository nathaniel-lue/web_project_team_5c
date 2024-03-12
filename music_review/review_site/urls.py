from django.urls import path, include
from .views import *

app_name = 'review_site'

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")), # authentication URLs
    path('accounts/register/', register, name='register')
]




"""
Info on "django.contrib.auth.urls":
This URL list includes:
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']

Main source: https://docs.djangoproject.com/en/5.0/topics/auth/
source: https://docs.djangoproject.com/en/5.0/topics/auth/default/
"""