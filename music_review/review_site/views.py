from django.shortcuts import render
from review_site.models import *

# Create your views here.
#test commit
def index(request):
    review_list = MusicReview.objects.order_by('-rating')[:5]
    context_dict = {}
    context_dict['reviews'] = review_list
     
    return render(request, 'review_site/index.html', context=context_dict)

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
    return render(request, 'review_site/post_review.html')

def sign_up_page(request):
    return render(request, 'review_site/signup.html')
