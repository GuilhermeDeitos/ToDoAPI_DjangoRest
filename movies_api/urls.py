from django.urls import path
from .views import MovieApiView, MovieDetailApiView, getByYear, getByGenre, getByTitle

urlpatterns = [
    path('api/', MovieApiView.as_view(), name='api'),
    path('api/<int:movie_id>/', MovieDetailApiView.as_view(), name='movie-detail'),
    path('api/genre/<str:genre>/', getByGenre, name='movie-detail-by-genre'),
    path('api/year/<int:year>/', getByYear, name='movie-detail-by-year'),
    path('api/title/<str:title>/', getByTitle, name='movie-detail-by-title'),  
]