from django.db import models

# django automatically creates an ID field for the models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 5 stars rating
    
# since EP is structurally the same as album it just inherits from the album model
class EP(Album):
    pass
    


# abstarct class for models of song, single
class MusicEntity(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 5 stars rating

    class Meta:
        abstract = True
        
# stand alone single
class Single(MusicEntity):
    pass

# song which is part of an album
class Song(MusicEntity):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


 
    
class Gig(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 5 stars rating