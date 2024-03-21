from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from review_site import views as review_views

app_name = 'review_site'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),  
    path('accounts/', include('django.contrib.auth.urls')),  
    path('accounts/register/', review_views.register, name='register'),  
    path("explore/", views.explore, name='explore'),
    path("post_review/", views.post_review, name="post_review"),
    path('forum/<int:review_id>/', views.forum, name='forum'),
    path('content_page/<str:content_type>/<int:content_id>/', views.content_page, name="content_page"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)