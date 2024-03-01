from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg



# django automatically creates an ID field for the models

'''
Rating stuff
'''
class Rating(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE) not sure yet how user will be represented
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
Users, Artists
''' 

class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    



'''
Albums, songs, EPs, Gigs
''' 

class Album(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    
    def __str__(self):
        return self.name
    
# since EP is structurally the same as album it just inherits from the album model
class EP(Album):
    pass
    


# abstarct class for models of song, single
class MusicEntity(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    
    def __str__(self):
        return f"{self.artist}: {self.name}"

    class Meta:
        abstract = True
        
# stand alone single
class Single(MusicEntity):
    pass

# song which is part of an album
class Song(MusicEntity):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


class Gig(models.Model, RatingMixin):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.artist}: {self.venue} - {self.date}"
    
    
    




     