from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/todo', views.todo_page, name='todo_page'),
    path('api/todo_main', views.main_todo, name='main_todo'),
    path('api/delete/<int:task_id>', views.delete, name='delete'),
    path('api/change_status/<int:task_id>', views.change_status, name='change_status'),
]