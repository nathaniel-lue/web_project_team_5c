from review_site.models import Album
from django.shortcuts import render



def index(request):
    response = render(request, 'review_site/index.html')
    return response

def explore(request):
    album = Album.objects.all()
    response = render(request, 'review_site/explore.html')
    return response

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
    return JsonResponse({'Albums':list(albums.values())})

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

def login_page(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            return redirect(reverse('view:index'))
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
     else:
            return render(request, 'login.html')

def sign_up_page(request):
    return render(request, 'review_site/signup.html')

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

