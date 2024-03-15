from django.urls import path, include
from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'review_site'

urlpatterns = [
    path("explore/", explore, name='explore'),
    path("post_review/", post_review, name="post_review"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
