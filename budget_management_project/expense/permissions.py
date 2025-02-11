from rest_framework import permissions


class IsExpenseOwner(permissions.BasePermission):
    message = "이 지출을 수정할 권한이 없습니다."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
