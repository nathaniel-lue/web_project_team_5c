from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'review_site/index.html')

def explore(request):
    return render(request, 'review_site/explore.html')

def forum(request):
    return render(request, 'review_site/forum.html')

def artist_profile(request):
    return render(request, 'review_site/explore/artist_profile.html')

def leaderboard(request):
    return render(request, 'review_site/leaderboard.html')

def music(request):
    return render(request, 'review_site/music.html')

def post_review(request):
    return render(request, 'review_site/postreview.html')

def sign_up_page(request):
    return render(request, 'review_site/signup.html')
