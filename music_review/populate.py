import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','music_review.settings')
import django
django.setup()
from review_site.models import Artist, Rating, Album, EP, Single, Song, Gig, MusicReview

def populate():
    artists = [{'name': 'The Strokes'}, {'name': 'The Doors'}, {'name': 'The Chemical Brothers'}]
    albums = [{'artist': 'The Strokes', 'name': 'Is This It', 'release_date': '2001-07-30'},
              {'artist': 'The Doors', 'name': 'L.A. Woman', 'release_date': '1971-04-19'},
              {'artist': 'The Chemical Brothers', 'name': 'Surrender', 'release_date': '1999-01-01'}]

    songs = {'Is This It': [
        {'name': 'Is This It', 'release_date': '2001-06-30'},
        {'name': 'The Modern Age', 'release_date': '2001-06-30'},
        {'name': 'Soma', 'release_date': '2001-06-30'},
        {'name': 'Barely Legal', 'release_date': '2001-06-30'},
        {'name': 'Someday', 'release_date': '2001-06-30'},
        {'name': 'Alone, Together', 'release_date': '2001-06-30'},
        {'name': 'Last Nite', 'release_date': '2001-06-30'},
        {'name': 'Hard to Explain', 'release_date': '2001-06-30'},
        {'name': 'When It Started', 'release_date': '2001-06-30'},
        {'name': 'Trying Your Luck', 'release_date': '2001-06-30'},
        {'name': 'Take It or Leave It', 'release_date': '2001-06-30'}
        ],
        'L.A. Woman': [
            {'name': 'The Changeling', 'release_date': '1971-04-19'},
            {'name': 'Love Her Madly', 'release_date': '1971-04-19'},
            {'name': 'Been Down So Long', 'release_date': '1971-04-19'},
            {'name': 'Cars Hiss by My Window', 'release_date': '1971-04-19'},
            {'name': 'L.A. Woman', 'release_date': '1971-04-19'},
            {'name': 'LAmerica', 'release_date': '1971-04-19'},
            {'name': 'Hyacinth House', 'release_date': '1971-04-19'},
            {'name': 'Crawling King Snake', 'release_date': '1971-04-19'},
            {'name': 'The WASP (Texas Radio and the Big Beat)', 'release_date': '1971-04-19'},
            {'name': 'Riders on the Storm', 'release_date': '1971-04-19'}
        ],
        'Surrender': [
            {'name': 'Music: Response', 'release_date': '1999-06-22'},
            {'name': 'Under the Influence', 'release_date': '1999-06-22'},
            {'name': 'Out of Control', 'release_date': '1999-06-22'},
            {'name': 'Orange Wedge', 'release_date': '1999-06-22'},
            {'name': 'Let Forever Be', 'release_date': '1999-06-22'},
            {'name': 'The Sunshine Underground', 'release_date': '1999-06-22'},
            {'name': 'Asleep from Day', 'release_date': '1999-06-22'},
            {'name': 'Got Glint?', 'release_date': '1999-06-22'},
            {'name': 'Hey Boy Hey Girl', 'release_date': '1999-05-31'},
            {'name': 'Surrender', 'release_date': '1999-06-22'},
            {'name': 'Dream On', 'release_date': '1999-06-22'},
            {'name': 'The Private Psychedelic Reel', 'release_date': '1999-06-22'}
        ]}

    gigs = [{'artist': 'The Strokes', 'venue': 'The Barrowlands', 'date': '2002-03-02'},
            {'artist': 'The Vaccines', 'venue': 'O2 Academy Glasgow', 'date': '2024-02-25'},
            {'artist': 'Rick Astley', 'venue': 'The Hydro', 'date': '2024-03-27'}]

    singles = [{'artist': 'The Stone Roses', 'name': 'Sally Cinnamon', 'release_date': '1987-01-02'},
               {'artist': 'The Vaccines', 'name': 'Norgaard', 'release_date': '2011-04-14'},
               {'artist': 'Alice In Chains', 'name': 'Would?', 'release_date': '1992-10-29'}]

    eps = [{'artist': 'Oasis', 'name': 'Whatever', 'release_date': '1994-12-18'},
           {'artist': 'The Snuts', 'name': 'Dreams', 'release_date': '2023-07-01'}]

    for artist in artists:
        a = add_artist(artist['name'])

    for album in albums:
        a = add_artist(album['artist'])
        alb = add_album(a, album['name'], album['release_date'])
        for songAlbum, song_data in songs.items():
            if songAlbum == album['name']:
                for songElts in song_data:
                    add_song(a, songElts['name'], songElts['release_date'], alb)

    for gig in gigs:
        a = add_artist(gig['artist'])
        add_gig(a, gig['venue'], gig['date'])

    for single in singles:
        a = add_artist(single['artist'])
        add_single(a, single['name'], single['release_date'])

    for ep in eps:
        a = add_artist(ep['artist'])
        add_ep(a, ep['name'], ep['release_date'])

def add_artist(name):
    a = Artist.objects.get_or_create(name=name)[0]
    a.name = name
    a.save()
    return a

def add_album(artist, name, release_date):
    a = Album.objects.get_or_create(artist=artist, name=name, release_date=release_date)[0]
    a.artist = artist
    a.name = name
    a.release_date = release_date
    a.save()
    return a

def add_song(artist, name, release_date, album):
    song = Song.objects.get_or_create(artist=artist, name=name, release_date=release_date, album=album)[0]
    song.artist = artist
    song.name = name
    song.release_date = release_date
    song.album = album
    song.save()
    return song

def add_gig(artist, venue, date):
    g = Gig.objects.get_or_create(artist=artist, venue=venue, date=date, )[0]
    g.artist = artist
    g.venue = venue
    g.date = date
    g.save()
    return g

def add_single(artist, name, release_date):
    s = Single.objects.get_or_create(artist=artist, name=name, release_date=release_date)[0]
    s.artist = artist
    s.name = name
    s.release_date = release_date
    s.save()
    return s

def add_ep(artist, name, release_date):
    a = EP.objects.get_or_create(artist=artist, name=name, release_date=release_date)[0]
    a.artist = artist
    a.name = name
    a.release_date = release_date
    a.save()
    return a

if __name__ == '__main__':
    print('Starting population script...')
    populate()