from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser


# django automatically creates an ID field for the models

'''
Users, Artists
''' 
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    
class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

'''
Rating model and method
'''
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)]) # 5 star rating
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.content_object}: {self.rating} stars by {self.user}"
    
    
# class to calculate average ratings
class RatingMixin:
    ratings = GenericRelation(Rating)

    def add_rating(self, user, rating):
        content_type = ContentType.objects.get_for_model(self)
        Rating.objects.update_or_create(
            content_type=content_type, object_id=self.id, user=user,
            defaults={'rating': rating})

    def average_rating(self):
        return self.ratings.aggregate(Avg('rating')).get('rating__avg') or None
    
  
'''
Albums, songs, EPs, Gigs
'''

class CollectionEntity(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    album_art = models.ImageField(upload_to='album_art/', null=True, blank=True, default='album_art/default-cover-art.png')
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
    
class Album(CollectionEntity):
    pass
    
class EP(CollectionEntity):
    pass
    

# abstarct class for models of song, single
class MusicEntity(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    album_art = models.ImageField(upload_to='album_art/', null=True, blank=True, default='album_art/default-cover-art.png')
    
    def __str__(self):
        return f"{self.artist}: {self.name}"

    class Meta:
        abstract = True
        
# stand alone single
class Single(CollectionEntity):
    pass

# song which is part of an album
class Song(MusicEntity):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

#Song which is part of an EP
class EPTrack(MusicEntity):
    ep = models.ForeignKey(EP, on_delete=models.CASCADE)

class Gig(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.artist}: {self.venue} - {self.date}"
    
    

'''
Reviews, comments
''' 

class MusicReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='music_reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    music_item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.title} by {self.user.username}"

def average_rating_review(content_type, object_id):
    reviews = MusicReview.objects.filter(content_type=content_type, object_id=object_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    if average_rating is None:
        return None
    return round(average_rating, 2)
    

class Comment(models.Model):
    review = models.ForeignKey(MusicReview, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"


     