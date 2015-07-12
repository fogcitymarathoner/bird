from django.conf.urls import patterns, include, url, handler404, handler500
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tpages.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^tpages/admin', include(admin.site.urls)),
    url(r'^tpages/', include('tpages.urls', namespace='tpages')),

)

# custom error handlers
handler404 = 'errors.views.error404'
handler500 = 'errors.views.error500'