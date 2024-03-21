from review_site.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


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

def logged_out(request):
    return render(request, 'registration/log_out.html')
