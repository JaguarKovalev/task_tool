from rest_framework import permissions, viewsets

from .models import Task
from .permissions import TaskPermission
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
