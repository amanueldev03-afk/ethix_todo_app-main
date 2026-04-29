# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.get_todos, name="home"),  # Add this for root URL
    path("todos/", views.get_todos, name="get_todos"),
    path("todos/<int:todo_id>/", views.get_todo_by_id, name="get_todo_by_id"),
    path("todos/create/", views.create_todo, name="create_todo"),
    path("todos/<int:todo_id>/update/", views.update_todo, name="update_todo"),
    path("todos/<int:todo_id>/delete/", views.delete_todo, name="delete_todo"),
    path("todos/<int:todo_id>/toggle/", views.toggle_complete, name="toggle_complete"),
]