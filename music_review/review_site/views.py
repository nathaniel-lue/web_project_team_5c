from django.urls import reverse
from review_site.models import Album
from django.shortcuts import render, redirect
from review_site.models import *
from django.http import JsonResponse
import json
from .models import MusicReview


def index(request):
    review_list = MusicReview.objects.all().order_by('-rating')[:5]
    context_dict = {'reviews': review_list}
    return render(request, 'review_site/index.html', context=context_dict)

def explore(request):
    review_list = MusicReview.objects.all()
    context_dict = {'reviews': review_list}
    return render(request, 'review_site/explore.html', context=context_dict)

def filter(request):
    genre = request.Get.get('Genre')
    release_date = request.Get.get('Release date')
    artist_popularity =request.Get.get('Artist Popularity')
    rating = request.Get.get('Rating')
    album = Album.objects.all()
    if genre:
        album = album.filter(genre = genre)
    if release_date:
        album = album.filter(release_date= release_date)
    if artist_popularity:
        album = album.filter(artist_popularity = artist_popularity)
    if rating:
        album = album.filter(rating = rating)
    return JsonResponse({'Albums':list(album.values())})

def artist_profile(request):
    return render(request, 'review_site/explore/artist_profile.html')

def review(request):
     response = render(request, 'review.html')
     return response('review.html')

def leaderboard(request):
    return render(request, 'review_site/leaderboard.html')

def music(request):
    return render(request, 'review_site/music.html')

def post_review(request):
    return render(request, 'review_site/post_review.html')
  
  
def search(request):
    request.Get.get('query', '')
    if query:
        songs = Song.objects.filter(title__icontains=query)
        singer = Singer.objects.filter(artists=query)
        album = Album.objects.filter(albums=query)
        review_title = Review_title.objects.filter(titles=query)
    else:
        return render(request, 'homepage.html')

    dictionary = {'songs':songs, 'singer':singer, 'album':album, 'review_title':review_title}

    return render(request, 'resultpage.html', dictionary)