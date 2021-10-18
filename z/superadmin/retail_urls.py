from django.conf.urls import url
from . import retail_views

urlpatterns = [
	url(r'^list$', retail_views.list),
	url(r'^create$', retail_views.create),
]