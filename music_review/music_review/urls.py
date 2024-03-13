from django.contrib import admin
from django.urls import path, include
from django.urls import path
from review_site import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('review_site.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  #move all the stuff below to review_site/urls.py
    # path('', views.index, name='index'),
    # path("explore/", views.explore, name='explore'),
    # path("post_review/", views.post_review , name = "post_review")

