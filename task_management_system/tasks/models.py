from django.contrib.auth.models import Group, User
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("pending", "Pending"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    deadline = models.DateTimeField(blank=True, null=True)
    shared_with = models.ManyToManyField(User, related_name="shared_tasks", blank=True)
    shared_groups = models.ManyToManyField(
        Group, related_name="group_tasks", blank=True
    )

    def __str__(self):
        return self.title
