from review_site.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


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




# Not sure if this is needed or not - Will update as I get more stuff done with authentication
# def login_page(request):
#      if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(username=username, password=password)
        
#         if user:
#             return redirect(reverse('index'))
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#      else:
#             return render(request, 'login.html')