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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
