from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.

class TodoApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    #Get all
    def get(self, request, *agrs, **kwargs):
        todos = Todo.objects.filter(user=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def post(self, request, *agrs, **kwargs):
       data = {
           'title': request.data.get('title'),
           'completed': request.data.get('completed'),
            'user': request.user.id
       }
       serializer = TodoSerializer(data=data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TodoDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        '''
        Método para auxiliar as outras funções, ele pega o objeto a partir do id de usuário e id da tarefa
        ''' 
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            raise Http404
        
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Obtem uma tarefa a partir do id da tarefa e do id do usuário caso exista
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res":"Não foi encontrado uma tarefa com esse id"},status=status.HTTP_404_BAD_REQUEST)
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    def put(self, request,todo_id, *agrs, **kwargs):
        '''
        Atualiza uma tarefa a partir do id da tarefa e do id do usuário caso exista
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res":"Não foi encontrado uma tarefa com esse id"},status=status.HTTP_404_BAD_REQUEST)
        data = request.data
        serializer = TodoSerializer(instance=todo_instance,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id, *agrs, **kwargs):
        '''
        Deleta uma tarefa a partir do id da tarefa e do id do usuário caso exista
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res":"Não foi encontrado uma tarefa com esse id"},status=status.HTTP_404_BAD_REQUEST)
        todo_instance.delete()
        return Response(
            {"res":"Tarefa deletada com sucesso"},
            status=status.HTTP_200_OK
        )


    

        
