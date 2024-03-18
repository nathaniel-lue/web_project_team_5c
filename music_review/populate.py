import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','music_review.settings')
import django
django.setup()
from review_site.models import Artist, Rating, Album, EP, Single, Song, Gig, MusicReview, EPTrack, CustomUser, MusicReview, ContentType, Comment
from django.core.files import File

def populate():
    artists = [{'name': 'The Strokes'}, {'name': 'The Doors'}, {'name': 'The Chemical Brothers'}, {'name': 'Stevie Wonder'}]
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
    
    epSongs = {"Whatever": [{'name': 'Whatever', 'release_date': '1994-12-18'},
                            {'name': "(It's Good) To Be Free", 'release_date': '1994-12-18'},
                            {'name': "Half The World Away", 'release_date': '1994-12-18'},
                            {'name': "Slide Away", 'release_date': '1994-12-18'} 
               ],
               "Dreams": [{'name': 'Dreams', 'release_date': '2023-07-01'},
                          {'name': 'Gloria', 'release_date': '2023-07-01'}]
               }
    
    users = [{'username': 'craig.sinc', 'password': '12345', 'email': '123@gmail.com', 'bio': 'Hi!'},
             {'username': 'Jim Bob', 'password': '2468', 'email': '12345@gmail.com', 'bio': 'Music lover.'},
             {'username': 'Dave Smith', 'password': '789', 'email': '123456@gmail.com', 'bio': 'I like music!'}]

    music_reviews = [{'user': 'craig.sinc', 'rating': 4.5, 'title': 'My Review of Is This It', 'content': 'I loved this album very much!', 'type': 'album', 'name': 'Is This It'},
    {'user': 'Jim Bob', 'title': 'My Review of Surrender', 'rating': 4.3, 'content': 'I loved this album very much!', 'type': 'album', 'name': 'Surrender'},
    {'user': 'Dave Smith', 'title': 'My Review of Whatever, the EP', 'rating': 4.2, 'content': 'This is my fave Oasis EP!', 'type': 'ep', 'name': 'Whatever'}
    ]
    
    music_ratings = [{'user': 'Jim Bob', 'rating': 4.2, 'type': 'song', 'name': 'Love Her Madly'},
                     {'user': 'craig.sinc', 'rating': 4.7, 'type': 'album', 'name': 'Is This It'},
                     {'user': 'Jim Bob', 'rating': 3.6, 'type': 'ep', 'name': 'Dreams'}]
    
    comments = [{'user': 'Dave Smith', 'content': 'I agree, I loved this too!', 'review': 'My Review of Is This It'},
                {'user': 'craig.sinc', 'content': 'I disagree, I did not like it at all...', 'review': 'My Review of Surrender'},
                {'user': 'Dave Smith', 'content': 'Agreed Jim, this track is great!', 'review': 'My Review of Surrender'}]
    
    
    for user in users:
        add_user(user['username'], user['password'], user['email'], user['bio'])
    
    for album in albums:
        a = add_artist(album['artist'])
        alb = add_album(a, album['name'], album['release_date'])
        for songAlbum, song_data in songs.items():
            if songAlbum == album['name']:
                for songElts in song_data:
                    add_song(a, songElts['name'], songElts['release_date'], alb)  

    for artist in artists:
        a = add_artist(artist['name'])

    for gig in gigs:
        a = add_artist(gig['artist'])
        add_gig(a, gig['venue'], gig['date'])

    for single in singles:
        a = add_artist(single['artist'])
        add_single(a, single['name'], single['release_date'])

    for ep in eps:
        a = add_artist(ep['artist'])
        e = add_ep(a, ep['name'], ep['release_date'])
        for epSong, song_data in epSongs.items():
            if epSong == ep['name']:
                for songElts in song_data:
                    add_ep_song(a, songElts['name'], songElts['release_date'], e)
                    
    for review in music_reviews:
        add_review(review['user'], review['title'], review['content'], review['type'], review['name'], review['rating'])
        
    for rating in music_ratings:
        add_rating(rating['user'], rating['rating'], rating['type'], rating['name'])
        
    for comment in comments:
        add_comment( comment['review'], comment['user'], comment['content'])

def add_artist(name):
    a = Artist.objects.get_or_create(name=name)[0]
    a.name = name
    a.save()
    return a

def add_user(username, password, email, bio):
    u = CustomUser.objects.get_or_create(username=username, password=password, email=email,bio=bio)[0]
    u.username = username
    u.password = password
    u.email = email
    u.bio = bio
    u.save()
    return u

album_art_directory = 'static/images/'
album_images = {'Is This It': 'isthisit.png', 'Whatever': 'Whatever.png', 'Surrender': 'hbhg.jpg'}

def add_album(artist, name, release_date):
    a = Album.objects.get_or_create(artist=artist, name=name, release_date=release_date)[0]
    a.artist = artist
    a.name = name
    if name in album_images:
        file_path = os.path.join(album_art_directory, album_images[name])
        with open(file_path, 'rb') as file:
            django_file = File(file)
            a.album_art.save(album_images[name], django_file, save=True)
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

    if name in album_images:
        file_path = os.path.join(album_art_directory, album_images[name])
        with open(file_path, 'rb') as file:
            django_file = File(file)
            a.album_art.save(album_images[name], django_file, save=True)
    a.save()
    return a

def add_ep_song(artist, name, release_date, ep):
    s = EPTrack.objects.get_or_create(artist=artist, name=name, release_date=release_date, ep=ep)[0]
    s.artist = artist
    s.name = name
    s.release_date = release_date
    s.ep = ep
    s.save()
    return s

def add_review(user, title, content, content_type, name, rating):
    u = CustomUser.objects.get(username=user)
    if(content_type=='album'):
        music_type = Album.objects.get(name=name)
    elif(content_type=='ep'):
        music_type = EP.objects.get(name=name)
    else:
        music_type = Song.objects.get(name=name)
    object_id = music_type.id
        
    content_type_obj = ContentType.objects.get_for_model(music_type.__class__)
    r =MusicReview.objects.get_or_create(user=u, title=title, content=content, content_type=content_type_obj, object_id = object_id, rating=rating)[0]
    
    r.user = u
    r.title = title
    r.content = content
    r.content_type = content_type_obj
    r.object_id = object_id
    r.rating = rating
    r.save()
    return r

def add_rating(user, rating, content_type, name):
    u = CustomUser.objects.get(username=user)
    if(content_type=='album'):
        music_type = Album.objects.get(name=name)
    elif(content_type=='ep'):
        music_type = EP.objects.get(name=name)
    else:
        music_type = Song.objects.get(name=name)
        
    object_id = music_type.id
    content_type_obj = ContentType.objects.get_for_model(music_type.__class__)
    r = Rating.objects.get_or_create(user=u, rating=rating, content_type = content_type_obj, object_id=object_id)[0]
    r.user = u
    r.rating = rating
    r.content_type = content_type_obj
    r.object_id = object_id
    r.save()
    return r

def add_comment(review, user, content):
    u = CustomUser.objects.get(username=user)
    r = MusicReview.objects.get(title=review)
    c = Comment.objects.get_or_create(review=r, user=u, content=content)[0]
    c.user = u
    c.review = r
    c.content = content
    c.save()
    return c

if __name__ == '__main__':
    print('Starting population script...')
    populate()
