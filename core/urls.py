from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("todos/", views.get_todos, name="get_todos"),
    path("todos/<int:todo_id>/", views.get_todo_by_id, name="get_todo_by_id"),
    path("todos/create/", views.create_todo, name="create_todo"),
]
