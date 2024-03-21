from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'review_site'

urlpatterns = [
    path('', views.index, name='index'),
    path("explore/", views.explore, name='explore'),
    path("post_review/", views.post_review, name="post_review"),
    path('forum/<int:review_id>/', views.forum, name='forum'),
    path('music/', views.music, name="music"),
    path('content_page/<str:content_type>/<int:content_id>/', views.content_page, name="content_page"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
