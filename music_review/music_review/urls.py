from django.contrib import admin
from django.urls import path, include
from django.urls import path
from music_review import views as project_views
from review_site import views as app_views
from django.conf import settings
from django.conf.urls.static import static
from review_site.views import register


urlpatterns = [
    path('', app_views.index, name='index'),
    path("admin/", admin.site.urls),
    path('reviews/', include('review_site.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/register/', register, name='register'),
    path('user_profile/<int:user_id>', project_views.show_profile, name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

