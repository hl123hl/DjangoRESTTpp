import uuid

from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from Admin.authentication import AdminUserAuthentiction
from Cinema.authentication import CinemaUserAuthentication
from Cinema.models import CinemaUser, CinemaMovieOrder, Hall
from Cinema.permisson import AdminUserPermission, CinemaMovieOrderermission
from Cinema.serializers import CinemaUserSerializer, CinemaMovieOrderSerializer
from Common.models import Movie
from utils.user_token_util import generate_cinema_token


class CinemaUserAPIView(ListCreateAPIView):
    queryset =  CinemaUser.objects.all()
    serializer_class =  CinemaUserSerializer
    authentication_classes = (AdminUserAuthentiction,)
    permission_classes = (AdminUserPermission,)


    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        if action == 'register':
            return self.create(request,*args,**kwargs)
        elif action == 'login':
            return self.do_login(request,*args,**kwargs)
        else:
            raise APIException(detail="请提供正确的动作")

    def do_login(self,request,*args,**kwargs):
        c_username = request.data.get("c_username")
        c_password = request.data.get("c_password")
        users = CinemaUser.objects.filter(c_username=c_username)
        if not users.exists():
            raise  APIException(detail="不存在")
        user = users.first()
        if not user.check_password(c_password):
            raise APIException(detail="密码不对")

        if user.is_delete:

            raise APIException(detail="用户以删除")
        token = generate_cinema_token()
        cache.set(token,user.id,timeout=60*60*24*7)
        data = {
            "msg":"ok",
            "status":HTTP_200_OK,
            "token":token
        }
        return Response(data)



class CinemaMovieOrderAPIView(ListCreateAPIView):
    queryset = CinemaMovieOrder.objects.all()
    serializer_class = CinemaMovieOrderSerializer
    authentication_classes = (CinemaUserAuthentication,AdminUserAuthentiction)
    permission_classes = (CinemaMovieOrderermission,)

    def get_queryset(self):
        queryset = super(CinemaMovieOrderAPIView,self).get_queryset()
        user = self.request.user
        if isinstance(user,CinemaUser):
            queryset = queryset.filter(c_user_id=user.id)
        return queryset
    def post(self, request, *args, **kwargs):
        movie_id = request.data.get("c_movie_id")
        movie = Movie.objects.get(pk=movie_id)
        c_price = movie.m_price
        self.request.c_price = c_price
        self.request.c_movie_id = movie_id
        orders = CinemaMovieOrder.objects.filter(c_movie_id=movie_id).filter(c_user_id=request.user.id)
        if orders.exists():
            raise APIException(detail="已购买")

        return self.create(self,*args,**kwargs)










class HallAPIView(ListCreateAPIView):
    queryset = Hall.objects.all()
    pass