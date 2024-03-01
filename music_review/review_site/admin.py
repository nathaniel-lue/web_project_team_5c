from django.contrib import admin
from .models import *


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'rating')
    list_filter = ('artist', 'release_date')
    search_fields = ('name', 'artist__name')

class EPAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'rating')
    list_filter = ('artist', 'release_date')
    search_fields = ('name', 'artist__name')

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album', 'release_date', 'rating')
    list_filter = ('artist', 'album', 'release_date')
    search_fields = ('name', 'artist__name', 'album__name')

class SingleAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'rating')
    list_filter = ('artist', 'release_date')
    search_fields = ('name', 'artist__name')

class GigAdmin(admin.ModelAdmin):
    list_display = ('artist', 'venue', 'rating')
    list_filter = ('artist', 'venue')
    search_fields = ('artist__name', 'venue')


# Register the models and their admin classes
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(EP, EPAdmin)  # If EPs are managed similarly to Albums
admin.site.register(Song, SongAdmin)
admin.site.register(Single, SingleAdmin)
admin.site.register(Gig, GigAdmin)


'''
list_display is used to specify which fields are shown in the list view of each model.

list_filter allows filtering by specified fields in the admin's list view sidebar.

search_fields enables search functionality on specified fields. Note that when searching through 
foreign key fields, you should use the syntax fieldname__relatedfieldname.
'''