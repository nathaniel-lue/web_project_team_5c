from django.urls import reverse
from review_site.models import Album
from django.shortcuts import render, redirect
from review_site.models import *
from django.http import JsonResponse
from django.contrib.auth import login
from .models import MusicReview
from review_site.forms import CommentCreationForm, ReviewCreationForm, UserCreationForm
from .models import MusicReview, Album, Comment, Song, Single, Artist, EP
from django.shortcuts import render
from .models import Song, Single, Album, MusicReview
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import json

def index(request):
    """Display the homepage with the latest reviews."""
    review_one = MusicReview.objects.all().order_by('-rating')[0]
    review_two = MusicReview.objects.all().order_by('-rating')[1]
    review_three = MusicReview.objects.all().order_by('-rating')[2]

    return render(request, 'review_site/index.html', {'review_one': review_one,'review_two': review_two,'review_two':review_three})

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

def post_review(request):
    context_dict = {}
    if request.method == 'POST':
        form = ReviewCreationForm(request.POST, request.FILES)
        context_dict['form'] = form
        if form.is_valid():
            posted_review = form.save(commit=False)
            review_type = form.cleaned_data['review_type']
            artist_name = form.cleaned_data['artist']
            music_title = form.cleaned_data['content_title']
            review_title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            rating = form.cleaned_data['rating']
            release_date = form.cleaned_data['release_date']
            
            if release_date == "" or release_date == None:
                release_date = "2000-01-01" # Give a default value for the release date if not given
                
                
                
            album_art = ""
            if ('album_upload' in request.FILES):
                album_art = request.FILES['album_upload']
            u = request.user
            posted_review.user = u

            # Get/create artist and relevant album/ep/single object 
            try:
                artist_obj = Artist.objects.get_or_create(name=artist_name)[0]
                if (review_type == "Album"):
                    album_obj = Album.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date)[0] 
                    if(album_art != ""): 
                        album_obj.album_art = album_art    
                    album_obj.save()
                    content_obj = album_obj
                elif (review_type == "EP"):
                    content_obj = EP.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date)[0]
                else:
                    content_obj = Single.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date)[0]
            except Exception as e:
                print("Error occurred " + e)
                return redirect('review_site:explore')

            object_id = content_obj.id
            content_type_obj = ContentType.objects.get_for_model(content_obj.__class__)
            
            posted_review.title = review_title
            posted_review.content = content
            posted_review.rating = rating
            posted_review.content_type = content_type_obj
            posted_review.object_id = object_id
            posted_review.save() 
            return redirect('review_site:explore')
    else:
        form = ReviewCreationForm()
        context_dict['form'] = form
    
    return render(request, 'review_site/post_review.html', context=context_dict)

def artist_profile(request):
    return render(request, 'review_site/explore/artist_profile.html')

def review(request):
     response = render(request, 'review.html')
     return response('review.html')

def leaderboard(request):
    return render(request, 'review_site/leaderboard.html')

def music(request):
    return render(request, 'review_site/music.html')
  
  
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
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)    
            return redirect('review_site:explore')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})