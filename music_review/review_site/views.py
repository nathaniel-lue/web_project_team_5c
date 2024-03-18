from django.urls import reverse
from review_site.models import Album
from django.shortcuts import render, redirect
from review_site.models import *
from django.http import JsonResponse
import json
from .models import MusicReview
from review_site.forms import CommentCreationForm
from .models import MusicReview, Album, Comment
from django.shortcuts import render
from .models import Song, Single, Album, MusicReview
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    """Display the homepage with the latest reviews."""
    review_list = MusicReview.objects.all().order_by('-rating')[:5]
    return render(request, 'review_site/index.html', {'reviews': review_list})

def explore(request):
    """Display a page to explore all reviews."""
    review_list = MusicReview.objects.all()
    return render(request, 'review_site/explore.html', {'reviews': review_list})

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

def forum(request, review_id):
    try:
        review = MusicReview.objects.get(id=review_id)
    except MusicReview.DoesNotExist:
        review = None

    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            posted_comment = form.save(commit=False)
            posted_comment.review = review
            posted_comment.user = request.user
            posted_comment.save()
            return redirect('review_site:forum', review_id=review_id)
    else:
        form = CommentCreationForm()
        comments = Comment.objects.filter(review=review) if review else []

    return render(request, 'review_site/forum.html', {'review': review, 'comments': comments, 'form': form})



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
    """Display a form for posting a new review and handle the submission."""
    return render(request, 'review_site/post_review.html')
  
  
def search(request):
    query = request.GET.get('query', '')

    context = {}

    if query:
        context['songs'] = Song.objects.filter(title__icontains=query)
        context['singer'] = Single.objects.filter(artists__icontains=query) 
        context['album'] = Album.objects.filter(albums__icontains=query) 
        context['review'] = MusicReview.objects.filter(titles__icontains=query)  
        return render(request, 'resultpage.html', context)
    else:
        return render(request, 'homepage.html')