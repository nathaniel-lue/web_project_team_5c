from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('explore')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
