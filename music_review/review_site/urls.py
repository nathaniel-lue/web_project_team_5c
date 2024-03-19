from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from review_site import views as app_views
from . import views

app_name = 'review_site'

urlpatterns = [
    path('', views.index, name='index'),
    path("admin/", admin.site.urls),
    path('', include('review_site.urls', namespace='review_site')),
    path('reviews/', include('review_site.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/register/', views.register, name='register'),
    path("explore/", views.explore, name='explore'),
    path("post_review/", views.post_review, name="post_review"),
    path('forum/<int:review_id>/', views.forum, name='forum'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
