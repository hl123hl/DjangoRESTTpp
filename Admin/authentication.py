from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException

from Admin.models import AdminUser


class AdminUserAuthentiction(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get("token")
            if not token.startswith("admin"):
                raise APIException(detail="用户信息不对等")
            user_id = cache.get("token")
            print(token,user_id)
            user = AdminUser.objects.get(pk=user_id)
            return user,token
        except Exception as e :
            return None