from rest_framework.permissions import BasePermission

from Admin.models import AdminUser

#超级管理员的权限
class SuperAdminPermission(BasePermission):
    SAFE_METHODS = ['GET','HEAD','OPTIONS']
    def has_permission(self, request, view):

        if request.method not in self.SAFE_METHODS:
            user = request.user
            return  isinstance(user,AdminUser) and user.is_super
            # if isinstance(user,AdminUser) and user.is_super:
            #
            #     return True
            # return  False
        return True
