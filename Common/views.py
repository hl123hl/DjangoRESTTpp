from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView


from Common.models import Movie
from Common.serializers import MovieSerializer
from Admin.authentication import AdminUserAuthentiction
from Admin.permissions import SuperAdminPermission
class MoviesAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    authentication_classes = (AdminUserAuthentiction,)
    #权限验证
    permission_classes = (SuperAdminPermission,)