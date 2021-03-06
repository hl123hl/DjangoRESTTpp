from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from Cinema.models import CinemaUser
from utils.user_token_util import CINEMA


class CinemaUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get("token")
            if not token.startwith(CINEMA):
                raise  Exception("认证失败")
            user_id = cache.get(token)
            user = CinemaUser.objects.filter(pk=user_id)
            return user,token
        except Exception as e:
            return None