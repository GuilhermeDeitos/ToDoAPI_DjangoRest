
from django.urls import path, include
from .views import (TodoApiView, TodoDetailApiView)
urlpatterns = [
    path('api/', TodoApiView.as_view(), name='api'),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view(), name='todo-detail'),
    
]