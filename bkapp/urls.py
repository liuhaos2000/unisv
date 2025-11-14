# bkapp/urls.py
from django.urls import path
from .views import ListCreateTodo, DetailUpdateTodo

urlpatterns = [
    path('todos/', ListCreateTodo.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', DetailUpdateTodo.as_view(), name='todo-detail-update'),
]
