from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^lost_password/', views.lost_password),
    url(r'^reset_password/', views.reset_password),
]