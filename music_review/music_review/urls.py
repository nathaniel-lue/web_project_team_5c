from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('review_site.urls'))
]

  #move all the stuff below to review_site/urls.py
    # path('', views.index, name='index'),
    # path("explore/", views.explore, name='explore'),
    # path("post_review/", views.post_review , name = "post_review")

