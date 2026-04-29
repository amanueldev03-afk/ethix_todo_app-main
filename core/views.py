# core/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Todo, User
from django.utils import timezone

def create_todo(request):
    print("=== CREATE TODO VIEW CALLED ===")
    print(f"Request method: {request.method}")
    
    if request.method == "POST":
        print("POST data:", request.POST)
        
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        user_id = request.POST.get("user_id")
        
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"User ID: {user_id}")
        
        # Validate inputs
        if not title:
            users = User.objects.all()
            return render(request, "create_todo.html", {
                "users": users, 
                "error": "Title is required!"
            })
        
        if not user_id:
            users = User.objects.all()
            return render(request, "create_todo.html", {
                "users": users, 
                "error": "Please select a user!"
            })
        
        try:
            # Get the user
            user = User.objects.get(username=user_id)
            print(f"Found user: {user}")
            
            # Create todo
            todo = Todo.objects.create(
                title=title,
                description=description,
                user=user
            )
            print(f"Created todo with ID: {todo.id}")
            
            # Redirect to todo list
            return redirect('core:get_todos')
            
        except User.DoesNotExist:
            print(f"User {user_id} not found!")
            users = User.objects.all()
            return render(request, "create_todo.html", {
                "users": users, 
                "error": f"User '{user_id}' not found!"
            })
    
    # GET request - show form
    users = User.objects.all()
    print(f"Users in database: {users.count()}")
    
    # Create a demo user if no users exist
    if users.count() == 0:
        print("No users found, creating demo user...")
        User.objects.create(
            username="demo", 
            email="demo@example.com", 
            password="demo123",
            bio="Demo user"
        )
        users = User.objects.all()
        print(f"Created demo user, now have {users.count()} users")
    
    return render(request, "create_todo.html", {"users": users})


def get_todos(request):
    print("=== GET TODOS VIEW CALLED ===")
    todos = Todo.objects.all().order_by('-created_at')
    print(f"Found {todos.count()} todos")
    
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
    print(f"=== GET TODO BY ID: {todo_id} ===")
    todo = get_object_or_404(Todo, pk=todo_id)
    return render(request, "detail.html", {"todo": todo})


def update_todo(request, todo_id):
    print(f"=== UPDATE TODO VIEW CALLED for ID: {todo_id} ===")
    todo = get_object_or_404(Todo, pk=todo_id)
    print(f"Todo title: {todo.title}")
    
    if request.method == "POST":
        print("POST data:", request.POST)
        
        # Get values from form
        new_title = request.POST.get("title")
        new_description = request.POST.get("description")
        is_completed = request.POST.get("is_completed") == "on"
        priority = request.POST.get("priority")
        
        print(f"New title: {new_title}")
        print(f"Is completed: {is_completed}")
        print(f"Priority: {priority}")
        
        # Update todo
        todo.title = new_title
        todo.description = new_description
        todo.is_completed = is_completed
        if priority:
            todo.priority = priority
        todo.save()
        
        print(f"Todo updated successfully!")
        return redirect('core:get_todos')
    
    return render(request, "update_todo.html", {"todo": todo})


def delete_todo(request, todo_id):
    print(f"=== DELETE TODO VIEW CALLED for ID: {todo_id} ===")
    todo = get_object_or_404(Todo, pk=todo_id)
    print(f"Todo to delete: {todo.title}")
    
    if request.method == "POST":
        print("DELETE CONFIRMED!")
        todo.delete()
        print("Todo deleted successfully!")
        return redirect('core:get_todos')
    
    return render(request, "delete_todo.html", {"todo": todo})


def toggle_complete(request, todo_id):
    print(f"=== TOGGLE COMPLETE for ID: {todo_id} ===")
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    print(f"Todo is now {'completed' if todo.is_completed else 'incomplete'}")
    return redirect('core:get_todos')