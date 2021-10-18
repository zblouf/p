from django.conf.urls import include, url
from z.superadmin.views import main

urlpatterns = [
    url(r'^account/', include('z.superadmin.account_urls')),
    url(r'^retail/', include('z.superadmin.retail_urls')),
    url(r'^db/', include('z.superadmin.db_urls')),
    url(r'^import/', include('z.superadmin.import_urls')),

    url(r'^main$', main),

]