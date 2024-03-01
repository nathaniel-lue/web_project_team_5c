from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


# Inline for Ratings
class RatingInline(GenericTabularInline):
    model = Rating
    extra = 1

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('bio', 'profile_picture')}),
    )

# Artist Admin
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Album and EP Admin
class AlbumAdmin(admin.ModelAdmin):
    inlines = [RatingInline,]
    list_display = ('name', 'artist', 'release_date')
    list_filter = ('artist', 'release_date')
    search_fields = ('name', 'artist__name')

class EPAdmin(AlbumAdmin):
    pass

# Music Entity Admin (for Song and Single)
class MusicEntityAdmin(admin.ModelAdmin):
    inlines = [RatingInline,]
    list_display = ('name', 'artist', 'release_date')
    list_filter = ('artist', 'release_date')
    search_fields = ('name', 'artist__name')

# Song Admin
class SongAdmin(MusicEntityAdmin):
    list_display = ('name', 'artist', 'album', 'release_date')

# Single Admin
class SingleAdmin(MusicEntityAdmin):
    pass

# Gig Admin
class GigAdmin(admin.ModelAdmin):
    inlines = [RatingInline,]
    list_display = ('artist', 'venue', 'date')
    list_filter = ('artist', 'venue', 'date')
    search_fields = ('artist__name', 'venue')

# Music Review Admin
class MusicReviewAdmin(admin.ModelAdmin):
    inlines = [RatingInline,]
    list_display = ('title', 'user', 'content_type')
    list_filter = ('user', 'content_type')
    search_fields = ('title', 'user__username')

# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'review', 'parent')
    list_filter = ('user', 'review')
    search_fields = ('user__username', 'review__title', 'content')


# Register the models and their admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(EP, EPAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Single, SingleAdmin)
admin.site.register(Gig, GigAdmin)
admin.site.register(MusicReview, MusicReviewAdmin)
admin.site.register(Comment, CommentAdmin)


'''
list_display is used to specify which fields are shown in the list view of each model.

list_filter allows filtering by specified fields in the admin's list view sidebar.

search_fields enables search functionality on specified fields. Note that when searching through 
foreign key fields, you should use the syntax fieldname__relatedfieldname.
'''