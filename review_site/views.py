from django.urls import reverse
from django.shortcuts import render, redirect
from review_site.models import *
from django.http import JsonResponse
from review_site.forms import CommentCreationForm, ReviewCreationForm
from .models import MusicReview, Album, Comment, Song, Single, Artist, EP
from itertools import chain
from django.template.loader import render_to_string
from review_site.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Q



def index(request):
    """Display the homepage with the latest reviews."""
    review_one = MusicReview.objects.all().order_by('-rating')[0]
    review_two = MusicReview.objects.all().order_by('-rating')[1]
    review_three = MusicReview.objects.all().order_by('-rating')[2]

    return render(request, 'review_site/index.html', {'review_one': review_one,'review_two': review_two,'review_three':review_three})



def filter_content_by_criteria(model, min_rating='', album_name='', artist_name=''):
    """
    Helper function for the explore view:
    Filter a given content type (Album, EP, Single) by minimum rating, album name, and artist name.

    Args:
    - model: The model class to filter (e.g., Album, EP, Single).
    - min_rating: The minimum average rating to filter by.
    - album_name: The name of the album to filter by.
    - artist_name: The artist's name to filter by.

    Returns:
    - A queryset of the filtered model instances.
    """
    content_type = ContentType.objects.get_for_model(model)
    objects = model.objects.all()

    if album_name:
        objects = objects.filter(name__icontains=album_name)
    if artist_name:
        objects = objects.filter(artist__name__icontains=artist_name)

    if min_rating:
        min_rating = float(min_rating)

        # Find IDs of objects that meet the minimum rating criteria
        filtered_ids = MusicReview.objects.filter(
            content_type=content_type,
            object_id__in=objects.values_list('id', flat=True)
        ).values('object_id').annotate(avg_rating=Avg('rating')).filter(avg_rating__gte=min_rating).values_list('object_id', flat=True)

        objects = objects.filter(id__in=filtered_ids)
    return objects


def explore(request):
    min_rating = request.GET.get('rating', '')
    album_name = request.GET.get('album_name', '')
    artist_name = request.GET.get('artist_name', '')

    filtered_albums = filter_content_by_criteria(Album, min_rating, album_name, artist_name)
    filtered_eps = filter_content_by_criteria(EP, min_rating, album_name, artist_name)
    filtered_singles = filter_content_by_criteria(Single, min_rating, album_name, artist_name)
    all_content = list(chain(filtered_albums, filtered_eps, filtered_singles))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('review_site/_explore_albums.html', {'all_content': all_content}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'review_site/explore.html', {'all_content': all_content, 'ratings': range(1, 6)})



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

def post_review(request, content_type=None, content_id=-1):
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
                    content_type_obj = ContentType.objects.get_for_model(Album)
                    album_obj = Album.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date, content_type=content_type_obj)[0] 
                    if(album_art != ""): 
                        album_obj.album_art = album_art    
                    album_obj.save()
                    content_obj = album_obj
                elif (review_type == "EP"):
                    content_type_obj = ContentType.objects.get_for_model(EP)
                    content_obj = EP.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date, content_type=content_type_obj)[0]
                    if(album_art != ""): 
                        content_obj.album_art = album_art    
                    content_obj.save()
                else:
                    content_type_obj = ContentType.objects.get_for_model(Single)
                    content_obj = Single.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date, content_type=content_type_obj)[0]
                    if(album_art != ""): 
                        content_obj.album_art = album_art    
                    content_obj.save()
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
        if "Album" in content_type:
            review_type = "Album"
            content_type_obj = ContentType.objects.get_for_model(Album)
            content_obj = Album.objects.filter(id=content_id)[0]
        elif "EP" in content_type:
            review_type = "EP"
            content_type_obj = ContentType.objects.get_for_model(EP)
            content_obj = EP.objects.filter(id=content_id)[0]
        else:
            review_type = "Single"
            content_type_obj = ContentType.objects.get_for_model(Single)
            content_obj = Single.objects.filter(id=content_id)[0]

        prepopulation = {
            'artist': content_obj.artist,
            'review_type': review_type,
            'content_title': content_obj.name,
            'release_date': content_obj.release_date
        }
        form = ReviewCreationForm(prepopulation)
        context_dict['form'] = form
    
    return render(request, 'review_site/post_review.html', context=context_dict)

def artist_profile(request):
    return render(request, 'review_site/explore/artist_profile.html')

def review(request):
     response = render(request, 'review.html')
     return response('review.html')

def leaderboard(request):
    return render(request, 'review_site/leaderboard.html')


def content_page(request, content_type, content_id):
    app_name, content_type_split = content_type.split('|')
    if "album" in str(content_type_split):
        content_type_obj = ContentType.objects.get_for_model(Album)
        content_obj = Album.objects.filter(id=content_id)
        average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(Album), object_id=content_id)
    elif "ep" in str(content_type_split):
        content_type_obj = ContentType.objects.get_for_model(EP)
        content_obj = EP.objects.filter(id=content_id)
        average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(EP), object_id=content_id)
    else:
        content_type_obj = ContentType.objects.get_for_model(Single)
        content_obj = Single.objects.filter(id=content_id)
        average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(Single), object_id=content_id)
        
    
    
    reviews = MusicReview.objects.filter(content_type=content_type_obj, object_id=content_id)

    # MusicReview.objects.filter(content_type=content_type, content_id=content_id)
    return render(request, 'review_site/content_page.html', {'reviews': reviews, 'content': content_obj, 'average_rating': average_rating})

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