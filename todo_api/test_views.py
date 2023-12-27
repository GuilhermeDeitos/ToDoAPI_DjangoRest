from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Todo
from .serializers import TodoSerializer
from django.contrib.auth.models import User

class TodoDetailApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.todo = Todo.objects.create(user=self.user, title='Test Todo', completed=False)

    def test_get_todo(self):
        url = reverse('todo-detail', kwargs={'todo_id': self.todo.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TodoSerializer(self.todo)
        self.assertEqual(response.data, serializer.data)

    def test_get_todo_not_found(self):
        url = reverse('todo-detail', kwargs={'todo_id': 999})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo(self):
        url = reverse('todo-detail', kwargs={'todo_id': self.todo.id})
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Todo', 'completed': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertEqual(self.todo.completed, True)

    def test_update_todo_not_found(self):
        url = reverse('todo-detail', kwargs={'todo_id': 999})
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Todo', 'completed': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo(self):
        url = reverse('todo-detail', kwargs={'todo_id': self.todo.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_delete_todo_not_found(self):
        url = reverse('todo-detail', kwargs={'todo_id': 999})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)