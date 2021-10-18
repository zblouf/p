from django.conf.urls import url
from z.superadmin import import_views

urlpatterns = [
    url(r'^$', import_views.home),

]