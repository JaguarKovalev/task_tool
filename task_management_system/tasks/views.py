from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .permissions import TaskPermission
from .serializers import GroupSerializer, TaskSerializer, UserSerializer


@method_decorator(csrf_exempt, name="dispatch")
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Кастомное действие для шеринга задачи
    @action(detail=True, methods=["POST"], url_path="share")
    def share_task(self, request, pk=None):
        task = self.get_object()
        users = request.data.get("users", [])
        groups = request.data.get("groups", [])

        # Добавление пользователей
        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
                task.shared_with.add(user)
            except User.DoesNotExist:
                return Response(
                    {"detail": f"User ID {user_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Добавление групп
        for group_id in groups:
            try:
                group = Group.objects.get(id=group_id)
                task.shared_groups.add(group)
            except Group.DoesNotExist:
                return Response(
                    {"detail": f"Group ID {group_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        task.save()
        return Response(
            {"detail": "Task shared successfully."}, status=status.HTTP_200_OK
        )

    # Кастомное действие для отмены шеринга задачи
    @action(detail=True, methods=["POST"], url_path="unshare")
    def unshare_task(self, request, pk=None):
        task = self.get_object()
        users = request.data.get("users", [])
        groups = request.data.get("groups", [])

        # Удаление пользователей
        for user_id in users:
            task.shared_with.remove(user_id)

        # Удаление групп
        for group_id in groups:
            task.shared_groups.remove(group_id)

        task.save()
        return Response(
            {"detail": "Access revoked successfully."}, status=status.HTTP_200_OK
        )
