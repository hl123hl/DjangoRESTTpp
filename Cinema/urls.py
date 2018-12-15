from django.conf.urls import url

from Cinema import views

urlpatterns = [
    url(r"^users/",views.CinemaUserAPIView.as_view()),
    url(r'^movieorders/$',views.CinemaMovieOrder)
]