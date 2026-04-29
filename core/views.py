# core/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Todo, User
from django.utils import timezone

def create_todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        user_id = request.POST.get("user_id")
        
        if title and user_id:
            user = get_object_or_404(User, pk=user_id)
            todo = Todo.objects.create(
                title=title,
                description=description,
                user=user
            )
            return redirect("core:get_todo_by_id", todo_id=todo.id)
    
    # For GET request, show create form
    users = User.objects.all()
    return render(request, "create_todo.html", {"users": users})


def get_todos(request):
    todos = Todo.objects.all().order_by('-created_at')
    newtodos = []
    for todo in todos:
        newtodos.append(
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "user": todo.user.username,
                "is_completed": todo.is_completed,
                "priority": todo.get_priority_display(),
            }
        )
    return render(request, "index.html", {"todo_lists": newtodos})


def get_todo_by_id(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    return render(request, "detail.html", {"todo": todo})


def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    
    if request.method == "POST":
        todo.title = request.POST.get("title", todo.title)
        todo.description = request.POST.get("description", todo.description)
        todo.is_completed = request.POST.get("is_completed") == "on"
        todo.priority = request.POST.get("priority", todo.priority)
        todo.save()
        return redirect("core:get_todo_by_id", todo_id=todo.id)
    
    return render(request, "update_todo.html", {"todo": todo})


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    
    if request.method == "POST":
        todo.delete()
        return redirect("core:get_todos")
    
    return render(request, "delete_todo.html", {"todo": todo})


def toggle_complete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("core:get_todos")