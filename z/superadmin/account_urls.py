from django.conf.urls import url
from z.superadmin import account_views

urlpatterns = [
    url(r'^list$', account_views.list),
    url(r'^create$', account_views.create),
    url(r'^(?P<aid>\d+)/home', account_views.detail_home),
    url(r'^(?P<aid>\d+)/entities', account_views.detail_entities),
    url(r'^(?P<aid>\d+)/apps', account_views.detail_apps),

]