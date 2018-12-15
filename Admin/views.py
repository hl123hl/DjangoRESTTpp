import uuid

from django.core.cache import cache

from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response

from Admin.authentication import AdminUserAuthentiction
from Admin.models import AdminUser, Permission
from Admin.permissions import SuperAdminPermission
from Admin.serializers import AdminUserSerializer, PermissionSerializer
#继承自CreateAPIView，只有post方法
from DjangoRESTTpp.settings import ADMIN_USER_TIMEOUT, ADMIN_USERS
from utils.user_token_util import generate_admin_token


class AdminUsersAPIView(CreateAPIView):
    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.filter(is_delete=False)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == 'register':
            return  self.create(request,*args,**kwargs)
        elif action == 'login':
            a_username = request.data.get("a_username")
            a_password = request.data.get("a_password")
            users = AdminUser.objects.filter(a_username=a_username)
            if not users.exists():
                raise APIException(detail="用户不在")
            user = users.first()
            if not user.check_admin_password(a_password):
                raise APIException(detail="密码不对")
            if user.is_delete:
                raise APIException(detail="用户离职")
            token = generate_admin_token()
            cache.set(token,user.id,timeout=ADMIN_USER_TIMEOUT)
            data = {
                "msg":"ok",
                "status":200,
                "token":token
            }
            return Response(data)
        else:
            raise APIException(detail="请求的方法不被允许")
    #重写perform_create，将一些内置的人创建为超级管理员
    def perform_create(self, serializer):
        a_username =  self.request.data.get("a_username")
        serializer.save(is_super = a_username in ADMIN_USERS)
        # if a_username in ADMIN_USERS:
        #     serializer.save(is_super=True)
        # else:
        #     serializer.save()

#权限许可


class PermissionsAPIView(ListCreateAPIView):
    queryset = Permission.objects.all()
    #序列化
    serializer_class = PermissionSerializer
    #用户验证
    authentication_classes = (AdminUserAuthentiction,)
    #权限验证
    permission_classes = (SuperAdminPermission,)

#修改权限
    def patch(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        permission_id = request.get("permission_id")
        try:
            permission = Permission.objects.get(pk=permission_id)
        except Exception as e:
            print(e)

            raise APIException(detail="没有权限")
        try:
            user = AdminUser.objects.get(pk=user_id)
        except Exception as e:

            raise APIException(detail="D")
        user.permission_set.add(permission)
        data = {
            "msg":"add success",
            'status':201
        }
        return Response(data)