import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Artist, Album, Song, Rating, MusicReview, Comment
from .forms import UserCreationForm, CommentCreationForm, ReviewCreationForm

class ArtistModelTests(TestCase):
    def test_artist_creation(self):
        artist = Artist.objects.create(name='Test Artist')
        self.assertEqual(artist.name, 'Test Artist')

class AlbumModelTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist')

    def test_album_creation(self):
        album = Album.objects.create(artist=self.artist, name='Test Album', release_date='2022-01-01')
        self.assertEqual(album.name, 'Test Album')

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

class ReviewSiteViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.artist = Artist.objects.create(name='Test Artist')

    def test_index_view(self):
        response = self.client.get(reverse('review_site:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the Music Review Site')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
    
class MusicReviewModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='reviewer', password='testpass123')
        self.artist = Artist.objects.create(name='Review Artist')
        self.album = Album.objects.create(artist=self.artist, name='Review Album', release_date='2022-01-01')

    def test_music_review_creation(self):
        review = MusicReview.objects.create(
            user=self.user,
            title='Great Album',
            content='This is a review content.',
            rating=4.5,
            music_item=self.album
        )
        self.assertEqual(review.title, 'Great Album')
        self.assertEqual(review.user.username, 'reviewer')

class CommentModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='commenter', password='testpass123')
        self.artist = Artist.objects.create(name='Comment Artist')
        self.album = Album.objects.create(artist=self.artist, name='Comment Album', release_date='2022-01-01')
        self.review = MusicReview.objects.create(
            user=self.user,
            title='Review for Comment',
            content='Review content here.',
            rating=4.0,
            music_item=self.album
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            review=self.review,
            user=self.user,
            content='This is a comment.'
        )
        self.assertEqual(comment.content, 'This is a comment.')
        self.assertEqual(comment.user.username, 'commenter')

class ReviewCreationFormTests(TestCase):
    def test_review_form_valid(self):
        form_data = {
            'title': 'Test Review',
            'content': 'Content of the test review.',
            'rating': 5,
        }
        form = ReviewCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

class CommentCreationFormTests(TestCase):
    def test_comment_form_valid(self):
        form_data = {'content': 'A test comment.'}
        form = CommentCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

class ExploreViewTests(TestCase):
    def test_explore_view_status_code(self):
        response = self.client.get(reverse('review_site:explore'))
        self.assertEqual(response.status_code, 200)

class PostReviewViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser2', password='password12345')
        self.client.login(username='testuser2', password='password12345')

    def test_post_review_view_status_code(self):
        response = self.client.get(reverse('review_site:post_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_site/post_review.html')

    def test_post_review_success(self):
        form_data = {
            'title': 'New Review',
            'content': 'Review content here.',
            'rating': 4.0,
        }
        response = self.client.post(reverse('review_site:post_review'), form_data)
        self.assertRedirects(response, reverse('review_site:explore'))

class SongModelTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist for Song')
        self.album = Album.objects.create(artist=self.artist, name='Test Album for Song', release_date='2023-01-01')

    def test_song_creation(self):
        song = Song.objects.create(artist=self.artist, name='Test Song', release_date='2023-01-02', album=self.album)
        self.assertEqual(song.name, 'Test Song')
        self.assertEqual(song.artist.name, 'Test Artist for Song')
        self.assertEqual(song.album.name, 'Test Album for Song')

    def test_song_str_representation(self):
        song = Song.objects.create(artist=self.artist, name='Test Song', release_date='2023-01-02', album=self.album)
        self.assertEqual(str(song), f'{song.artist}: {song.name}')

class RatingModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='rater', password='testpass1234')
        self.artist = Artist.objects.create(name='Artist for Rating')
        self.song = Song.objects.create(artist=self.artist, name='Song for Rating', release_date='2023-01-03')

    def test_rating_creation(self):
        rating = Rating.objects.create(user=self.user, rating=4.5, content_object=self.song)
        self.assertEqual(rating.rating, 4.5)
        self.assertEqual(rating.user.username, 'rater')
        self.assertEqual(rating.content_object, self.song)

    def test_average_rating_on_song(self):
        Rating.objects.create(user=self.user, rating=4.0, content_object=self.song)
        another_user = get_user_model().objects.create_user(username='another_rater', password='pass12345')
        Rating.objects.create(user=another_user, rating=5.0, content_object=self.song)
        song_average_rating = self.song.average_rating()
        self.assertEqual(song_average_rating, 4.5)

    def test_rating_str_representation(self):
        rating = Rating.objects.create(user=self.user, rating=4.5, content_object=self.song)
        expected_str = f"{rating.content_object}: {rating.rating} stars by {rating.user}"
        self.assertEqual(str(rating), expected_str)



if __name__ == '__main__':
    unittest.main()

