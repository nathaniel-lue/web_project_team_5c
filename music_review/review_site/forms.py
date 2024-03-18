from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError  
# from django.forms.fields import EmailField  
from .models import CustomUser, Comment, MusicReview, CustomUser

# Basic implementaion of creating a user registration form
# email stuff commented out for easier debugging

class UserCreationForm(UserCreationForm): 
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    #email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
    
    class Meta:
        model = CustomUser
        fields = ("username", #"email",
                  "password1", "password2")
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = CustomUser.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    # def email_clean(self):  
    #     email = self.cleaned_data['email'].lower()  
    #     new = User.objects.filter(email=email)  
    #     if new.count():  
    #         raise ValidationError(" Email Already Exist")  
    #     return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = CustomUser.objects.create_user(  
            username = self.cleaned_data['username'],  
            # email = self.cleaned_data['email'],  
            password = self.cleaned_data['password1']  
        )  
        return user  

class CommentCreationForm(forms.ModelForm):
    content = forms.CharField(max_length=150, help_text="Add a comment.")
    class Meta:
        model = Comment
        fields = ['content']

class ReviewCreationForm(forms.ModelForm):
    type_choices = [('Album', 'Album'),('Single', 'Single'),('EP', 'EP')]
    
    artist = forms.CharField(max_length=100, help_text="Artist")
    review_type = forms.ChoiceField(choices=type_choices)
    title = forms.CharField(max_length=100, help_text="Title of your review")
    content_title = forms.CharField(max_length=20, help_text="Title of music content being reviewed")
    content = forms.CharField(max_length=150, help_text="Write your review!")
    rating = forms.FloatField(min_value=0, max_value=5, help_text="0-5 Stars")
    release_date = forms.DateField(help_text="YYYY-MM-DD format", required=False)
    album_upload = forms.ImageField(required=False, help_text="Upload artwork for this review", )
    
    class Meta:
        model = MusicReview
        fields = ['artist', 'review_type', 'title', 'content_title', 'content', 'rating', 'release_date', 'album_upload']
    