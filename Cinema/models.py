from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
from Common.models import Movie

CINEMA_REGISTER = 0
CINEMA_ACTIVE = 1
CINEMA_CAN_CREATE = 2
CINEMA_CAN_DELETE = 4
class CinemaUser(models.Model):
    c_username = models.CharField(max_length=32,unique=True)
    c_password = models.CharField(max_length=256)
    is_delete = models.BooleanField(default=False)
    c_permission = models.IntegerField(default=CINEMA_REGISTER)
    #检测权限
    def check_permission(self,permission):
        #比较的是二进制& 相同为0 不同为1
        return self.c_permission & permission == permission

    def set_passwod(self,password):
        self.c_password = make_password(password)
    def check_password(self,password):
        return check_password(password,self.c_password)

ORDERD_NOT_PAY = 0 #已下单未付款
ORDERD_PAYED = 0  #已下单以付款
class CinemaMovieOrder(models.Model):

    c_user = models.ForeignKey(CinemaUser)
    c_movie = models.ForeignKey(Movie)
    #状态
    c_status = models.IntegerField(default=ORDERD_NOT_PAY)
    c_price  = models.FloatField(default=0)
    is_delete = models.BooleanField(default=False)

class Cinema(models.Model):
    c_name = models.CharField(max_length=64)
    c_address = models.CharField(max_length=128)
    c_phone = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)
    c_user = models.ForeignKey(CinemaUser)

#大厅
class Hall(models.Model):
    h_cinema = models.ForeignKey(Cinema)#影院
    h_name = models.CharField(max_length=32)#大厅名
    h_seats = models.CharField(max_length=256) #座位



