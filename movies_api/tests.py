from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Movie

class MovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie_data = {
            "title": "Test Movie",
            "release_year": 2022,
            "genre": "Test Genre",
            "director": "Test Director"
        }
        self.movie = Movie.objects.create(**self.movie_data)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.force_authenticate = self.client.force_authenticate(user=self.user)


    def test_list_movies(self):
        url = reverse("api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_single_movie_post(self):
        Movie.objects.all().delete()  # Limpa o banco de dados antes de cada teste
        url = reverse("api")
        response = self.client.post(url, self.movie_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)

    def test_multiple_movies_post(self):
        Movie.objects.all().delete()  # Limpa o banco de dados antes de cada teste
        url = reverse("api")
        movies_data = [
            {"title": "Movie1", "release_year": 2021, "genre": "Action", "director": "Director1"},
            {"title": "Movie2", "release_year": 2022, "genre": "Comedy", "director": "Director2"}
        ]

        response = self.client.post(url, movies_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)


    def test_get_movie_detail(self):
        url = reverse("movie-detail", args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_movie(self):
        url = reverse("movie-detail", args=[self.movie.id])
        updated_data = {
            "title": "Updated Movie",
            "release_year": 2023,
            "genre": "Updated Genre",
            "director": "Updated Director"
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, updated_data["title"])

    def test_delete_movie(self):
        url = reverse("movie-detail", args=[self.movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_get_movies_by_genre(self):
        url = reverse("movie-detail-by-genre", args=["Test Genre"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_by_year(self):
        url = reverse("movie-detail-by-year", args=[2022])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_by_title(self):
        url = reverse("movie-detail-by-title", args=["Test Movie"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

