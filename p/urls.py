from django.conf.urls import include, url
from django.contrib import admin

from z.core.main.views import root, home, springboard

urlpatterns = [
    url(r'^$', root),
    url(r'^home$', home),
    url(r'^springboard$', springboard),

    url(r'^auth/', include('z.auth.urls')),

    url(r'^_admin/', include('z.superadmin.urls')),

    # Examples:
    # url(r'^$', 'p.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
