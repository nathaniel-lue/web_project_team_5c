from django.contrib import admin
from django.urls import path, include
from review_site import views as app_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', app_views.index, name='index'),
    path("admin/", admin.site.urls),
    path('reviews/', include('review_site.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/register/',views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
