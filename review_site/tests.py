from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import MusicReview, Album, Artist, EP, Rating, Single, Comment, CustomUser, average_rating_review, Song
from .forms import CommentCreationForm, ReviewCreationForm, UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model



User = get_user_model() # should make the CustomUser model appear as User


class ViewWithDatabaseTest(TestCase):
    fixtures = ['review_site/fixtures/fixture.json'] # populates the class test environment with a copy of the current database
    
    def test_index_view(self):
        response = self.client.get(reverse('review_site:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Is This It')


class ReviewSiteViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.artist = Artist.objects.create(name='Test Artist')


    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
    
    
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------


class ModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', bio='A short bio')
        self.artist = Artist.objects.create(name='Test Artist')
        content_type = ContentType.objects.get_for_model(Album)
        self.album = Album.objects.create(artist=self.artist, name='Test Album', release_date='2000-01-01', content_type=content_type)

    def test_custom_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_artist_str(self):
        self.assertEqual(str(self.artist), 'Test Artist')

    def test_rating_creation_and_str(self):
        content_type = ContentType.objects.get_for_model(self.album)
        rating = Rating.objects.create(user=self.user, rating=4.5, content_type=content_type, object_id=self.album.id)
        self.assertEqual(str(rating), f'{self.album}: 4.5 stars by testuser')


    def test_album_average_rating(self):
        MusicReview.objects.create(user=self.user, title='Great Album', content='Loved it!', rating=5, content_type=ContentType.objects.get_for_model(self.album), object_id=self.album.id)
        MusicReview.objects.create(user=self.user, title='Great Album', content='okay', rating=3, content_type=ContentType.objects.get_for_model(self.album), object_id=self.album.id)
        self.assertEqual(average_rating_review(content_type=ContentType.objects.get_for_model(Album), object_id=self.album.id), 4)

    def test_music_review_creation(self):
        review = MusicReview.objects.create(user=self.user, title='Great Album', content='Loved it!', rating=4.5, content_type=ContentType.objects.get_for_model(self.album), object_id=self.album.id)
        self.assertEqual(str(review), 'Great Album by testuser')

    def test_comment_creation(self):
        review = MusicReview.objects.create(user=self.user, title='Great Album', content='Loved it!', rating=4.5, content_type=ContentType.objects.get_for_model(self.album), object_id=self.album.id)
        comment = Comment.objects.create(review=review, user=self.user, content='Agree with this review!')
        self.assertEqual(str(comment), f'Comment by testuser on Great Album')

    def test_invalid_rating(self):
        content_type = ContentType.objects.get_for_model(self.album)
        # Create the Rating instance without saving it to the database
        rating = Rating(user=self.user, rating=6, content_type=content_type, object_id=self.album.id)
        with self.assertRaises(ValidationError):
            rating.full_clean() # explicitly call full_clean() so the validators are used
            
            
class MusicReviewModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='reviewer', password='testpass123')
        self.artist = Artist.objects.create(name='Review Artist')
        content_type = ContentType.objects.get_for_model(Album)
        self.album = Album.objects.create(artist=self.artist, name='Review Album', release_date='2022-01-01', content_type=content_type)
        self.content_type1 = ContentType.objects.get_for_model(Album)
        self.object_id1 = self.album.id

    def test_music_review_creation(self):
        review = MusicReview.objects.create(
            user=self.user,
            title='Great Album',
            content='This is a review content.',
            rating=4.5,
            content_type=self.content_type1,
            object_id=self.object_id1
        )
        self.assertEqual(review.title, 'Great Album')
        self.assertEqual(review.user.username, 'reviewer')

class CommentModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='commenter', password='testpass123')
        self.artist = Artist.objects.create(name='Comment Artist')
        content_type = ContentType.objects.get_for_model(Album)
        self.album = Album.objects.create(artist=self.artist, name='Review Album', release_date='2022-01-01', content_type=content_type)
        self.review = MusicReview.objects.create(
            user=self.user,
            title='Review for Comment',
            content='Review content here.',
            rating=4.0,
            content_type = ContentType.objects.get_for_model(Album),
            object_id = self.album.id,
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            content='This is a comment.'
        )
        self.assertEqual(comment.content, 'This is a comment.')
        self.assertEqual(comment.user.username, 'commenter')
        
        
        
class ArtistModelTests(TestCase):
    def test_artist_creation(self):
        artist = Artist.objects.create(name='Test Artist')
        self.assertEqual(artist.name, 'Test Artist')

class AlbumModelTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist')

    def test_album_creation(self):
        content_type = ContentType.objects.get_for_model(Album)
        self.album = Album.objects.create(artist=self.artist, name='Review Album', release_date='2022-01-01', content_type=content_type)
        self.assertEqual(self.album.name, 'Review Album')

class UserModelTests(TestCase):
    def test_custom_user_creation(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)

class UserCreationFormTests(TestCase):
    def test_form_valid(self):
        form_data = {'username': 'newuser', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {'username': 'newuser', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        form = UserCreationForm(data=form_data)
        if form.is_valid():
            new_user = form.save()
            self.assertEqual(new_user.username, 'newuser')

class CommentCreationFormTests(TestCase):
    def test_comment_form_valid(self):
        form_data = {'content': 'A test comment.'}
        form = CommentCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewTest(TestCase):
    def setUp(self):
        # Set up data for testing
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
    def test_explore_view_without_parameters(self):
        response = self.client.get(reverse('review_site:explore'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'reviews')
        

class PostReviewViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser2', password='password12345')
        self.client.login(username='testuser2', password='password12345')

    def test_post_review_view_status_code(self):
        response = self.client.get(reverse('review_site:post_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_site/post_review.html')


class SongModelTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist for Song')
        content_type = ContentType.objects.get_for_model(Album)
        self.album = Album.objects.create(artist=self.artist, name='Test Album for Song', release_date='2022-01-01', content_type=content_type)

    def test_song_creation(self):
        song = Song.objects.create(artist=self.artist, name='Test Song', release_date='2023-01-02', album=self.album)
        self.assertEqual(song.name, 'Test Song')
        self.assertEqual(song.artist.name, 'Test Artist for Song')
        self.assertEqual(song.album.name, 'Test Album for Song')

    def test_song_str_representation(self):
        song = Song.objects.create(artist=self.artist, name='Test Song', release_date='2023-01-02', album=self.album)
        self.assertEqual(str(song), f'{song.artist}: {song.name}')

# # ------------------------------------------------------------------------------------------------------------------------------------------------------------

class AuthenticationTests(TestCase):
    # The only custom view
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complex_password',
            'password2': 'complex_password',
        })
        # Check that the response is a redirect (success)
        self.assertEqual(response.status_code, 302)
        # Verify that the user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        

#     # login is a part of django.contrib.auth.urls, so if this works, all the others work as well
    def test_login(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345',
        })
        # Check the response code (should be a redirect on successful login)
        self.assertEqual(response.status_code, 302)
        # Verify that the login actually occurred
        self.assertTrue('_auth_user_id' in self.client.session)

