from rest_framework import permissions


class IsAdminOrLibraryMan(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'LibraryMan' in tuple(map(lambda x: x.name, request.user.groups.all())):
            return True
        return bool(request.user and request.user.is_staff)


class IsAdminOrLibraryManOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if 'LibraryMan' in tuple(map(lambda x: x.name, request.user.groups.all())):
            return True
        return bool(request.user and request.user.is_staff)
