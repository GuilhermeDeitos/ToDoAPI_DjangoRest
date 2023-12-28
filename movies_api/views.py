from django import http
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Movie
from .serializers import MovieSerializer

msgNotFound = {
    "message": "Não encontrado"
}

class MovieApiView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            if serializer.data:
                return Response(
                    {
                        "message": "Filmes retornados com sucesso",
                        "res": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                msgNotFound,
                status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Não autorizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            movies = request.data
            if isinstance(movies, dict): 
                serializer = MovieSerializer(data=movies)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif isinstance(movies, list):  
                for movie in movies:
                    serializer = MovieSerializer(data=movie)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "Dados inválidos"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"message": "Filmes adicionados com sucesso",
                 "res": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MovieDetailApiView(APIView):
    
    def get_object(self, movie_id):
        '''
        Método para auxiliar as outras funções, ele pega o objeto a partir do id de usuário e id da tarefa
        ''' 
        try:
            return Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise http.Http404
        
    #GetById
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie_instance = self.get_object(movie_id)
            if not movie_instance:
                return Response(
                    msgNotFound,
                    status=status.HTTP_404_NOT_FOUND)
            
            serializer = MovieSerializer(movie_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except http.Http404:
            return Response(
                msgNotFound,
                status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, movie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Não autorizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            movie_instance = self.get_object(movie_id)
            if not movie_instance:
                return Response(
                    msgNotFound,
                    status=status.HTTP_404_NOT_FOUND
                    )  
            serializer = MovieSerializer(movie_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, movie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Não autorizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            movie_instance = self.get_object(movie_id)
            if not movie_instance:
                return Response(
                    msgNotFound,
                    status=status.HTTP_404_NOT_FOUND)
            
            movie_instance.delete()
            return Response(
                {"message": "Filme deletado com sucesso"},
                status=status.HTTP_204_NO_CONTENT
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    

#Outras buscas
@api_view(['GET'])
def getByGenre(request, genre, *args, **kwargs):
    try:
        movies = Movie.objects.filter(genre=genre)
        if not movies:
            return Response(msgNotFound,status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def getByYear(request, year, *args, **kwargs):
    try:
        movies = Movie.objects.filter(release_year=year)
        if not movies:
            return Response(msgNotFound,status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getByTitle(request, title, *args, **kwargs):
    try:
        movies = Movie.objects.filter(title=title)
        if not movies:
            return Response(msgNotFound,status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
