from django.conf.urls import url

from Common import views

urlpatterns = [
    url(r'^movies/',views.MoviesAPIView.as_view())
]