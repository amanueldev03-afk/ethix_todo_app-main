from django.http import HttpResponse
from django.shortcuts import render
from .models import Todo, User


def create_todo(request):
    return HttpResponse("Create a new todo")


def get_todos(request):
    todos = Todo.objects.all()
    newtodos = []
    for todo in todos:
        newtodos.append(
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "user": todo.user.username,
            }
        )
    print(newtodos)
    return render(request, "index.html", {"todo_lists": newtodos})


def get_todo_by_id(request, todo_id):
    find_todo = Todo.objects.get(pk=todo_id)
    if not find_todo:
        return HttpResponse("Todo not found", status=404)
    return render(request, "detail.html", {"todo": find_todo})


def update_todo(request):
    return HttpResponse("Update a todo")


def delete_todo(request):
    return HttpResponse("Delete a todo")