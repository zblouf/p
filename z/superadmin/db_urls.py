from django.conf.urls import url
from z.superadmin import db_views

urlpatterns = [
    url(r'^home$', db_views.home),
    url(r'^common$', db_views.common),
    url(r'^prev$', db_views.prev),
	#(r'^home$', 'home'),
    #(r'^home$', 'home'),
    #(r'^home$', 'home'),
    #(r'^home$', 'home'),
    #(r'^home$', 'home'),
    url(r'^domains$', db_views.domains_home),

]