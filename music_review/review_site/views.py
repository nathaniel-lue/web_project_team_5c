from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'review_site/index.html')

def explore(request):
    return render(request, 'review_site/explore.html')

