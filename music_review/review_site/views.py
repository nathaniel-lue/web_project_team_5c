from django.urls import reverse
from django.shortcuts import render, redirect
from review_site.models import *
from django.http import JsonResponse
from review_site.forms import CommentCreationForm, ReviewCreationForm
from .models import MusicReview, Album, Comment, Song, Single, Artist, EP
from django.template.loader import render_to_string


def index(request):
    """Display the homepage with the latest reviews."""
    review_one = MusicReview.objects.all().order_by('-rating')[0]
    review_two = MusicReview.objects.all().order_by('-rating')[1]
    review_three = MusicReview.objects.all().order_by('-rating')[2]

    return render(request, 'review_site/index.html', {'review_one': review_one,'review_two': review_two,'review_three':review_three})


def explore(request):
    """Display a page to explore all reviews."""
    # Get the rating from request parameters
    min_rating = request.GET.get('rating')
    album_name = request.GET.get('album_name', '')  # Default to empty string if not provided
    artist_name = request.GET.get('artist_name', '') # Default to empty string if not provided
    reviews = MusicReview.objects.all()

    # Filter by rating if applicable
    if min_rating:
        reviews = reviews.filter(rating__gte=int(min_rating))  # gte stands for 'greater than or equal to'
        
    # Get ContentType for Album model
    album_content_type = ContentType.objects.get_for_model(Album)

    # Initialize an empty Q object for complex querying
    from django.db.models import Q
    album_query = Q()

    if album_name:
        # Add album name condition to the album query
        album_query |= Q(name__icontains=album_name)

    if artist_name:
        # Add artist name condition to the album query
        album_query |= Q(artist__name__icontains=artist_name)

    if album_query:
        # Get IDs of Album instances that match the album and/or artist name criteria
        album_ids = Album.objects.filter(album_query).values_list('id', flat=True)
        # Filter MusicReview objects that are related to these Album instances
        reviews = reviews.filter(content_type=album_content_type, object_id__in=album_ids)
        
    # Use this to check if it's an ajax request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('review_site/_explore_albums.html', {'reviews': reviews}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'review_site/explore.html', {'reviews': reviews, 'ratings': range(1, 6),})


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
                    if(album_art != ""): 
                        content_obj.album_art = album_art    
                    content_obj.save()
                else:
                    content_obj = Single.objects.get_or_create(artist=artist_obj, name=music_title, release_date=release_date)[0]
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
            return redirect('review_site:music')
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
    albums_with_reviews = []
    albums_no_reviews = []

    try:
        all_albums = Album.objects.all()
        for album in all_albums:
            all_album_reviews = MusicReview.objects.filter(content_type=ContentType.objects.get_for_model(Album), object_id=album.id)
            if all_album_reviews.exists():
                average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(Album), object_id=album.id)
                albums_with_reviews.append((album, all_album_reviews, average_rating))
            else:
                albums_no_reviews.append(album)
                
        all_eps = EP.objects.all()
        for ep in all_eps:
            all_ep_reviews = MusicReview.objects.filter(content_type=ContentType.objects.get_for_model(EP), object_id=ep.id)
            if all_ep_reviews.exists():
                average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(EP), object_id=ep.id)
                albums_with_reviews.append((ep, all_ep_reviews, average_rating))
            else:
                albums_no_reviews.append(ep)
                
        all_singles = Single.objects.all()
        for single in all_singles:
            all_single_reviews = MusicReview.objects.filter(content_type=ContentType.objects.get_for_model(Single), object_id=single.id)
            if all_single_reviews.exists():
                average_rating = average_rating_review(content_type=ContentType.objects.get_for_model(Single), object_id=single.id)
                albums_with_reviews.append((single, all_single_reviews, average_rating))
            else:
                albums_no_reviews.append(single)   
    except Exception as e:
        pass
    return render(request, 'review_site/music.html', {'albums_with_reviews': albums_with_reviews, 'albums_no_reviews': albums_no_reviews})

  
  
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