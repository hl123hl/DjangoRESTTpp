from rest_framework.permissions import BasePermission

from Admin.models import AdminUser

#超级管理员的权限
from Cinema.models import CinemaUser


class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method  == "GET":
            user = request.user
            return  isinstance(user,AdminUser)
        return True


class CinemaMovieOrderermission(BasePermission):
    CINEMA_USER_METHODS = ["POST","DELETE"]

    def has_permission(self, request, view):
        if request.method == "GET":
            user = request.user
            return isinstance(user,CinemaUser) or isinstance(user,AdminUser)
        elif request.method in self.CINEMA_USER_METHODS:
            user = request.user
            return  isinstance(user,CinemaUser)
        return False

class CinemaPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user
            return isinstance(user,CinemaUser)
        return True
