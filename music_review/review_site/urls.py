from django.urls import path, include
from .views import *
from django.contrib import admin
from django.urls import path
from review_site import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'review_site'

urlpatterns = [
    path("explore/", views.explore, name='explore'),
    path("post_review/", views.post_review, name="post_review"),
    path('forum/<int:review_id>', views.forum, name='forum'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 




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