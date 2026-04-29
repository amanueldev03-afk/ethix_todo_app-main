# core/models.py
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=12, null=False, blank=False)
    bio = models.CharField(max_length=225, blank=True, null=True)  # Made optional

    def __str__(self):
        return self.username


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Fixed: auto_now_add for creation
    updated_at = models.DateTimeField(auto_now=True)  # Added missing field
    is_completed = models.BooleanField(default=False)

    class PRIORITY(models.TextChoices):
        HIGH = "H", "High"
        MEDIUM = "M", "Medium"
        LOW = "L", "Low"

    priority = models.CharField(
        max_length=1,
        choices=PRIORITY.choices,
        default=PRIORITY.LOW,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title