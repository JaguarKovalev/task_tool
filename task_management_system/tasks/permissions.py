from rest_framework.permissions import BasePermission


class TaskPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or request.user in obj.shared_with.all()
            or request.user.groups.filter(
                id__in=obj.shared_groups.values_list("id", flat=True)
            ).exists()
        )
