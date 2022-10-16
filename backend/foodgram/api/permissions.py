from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerAdminOrReadOnly(BasePermission):
    """Owner and admin permission."""

    message = 'Вы не являетесь автором или администратором!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user or request.user.is_staff
        )
