from django.conf.urls.defaults import *
from uploader import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'uploader.publics.views.index'),
	(r'^upload/$', 'uploader.publics.views.upload'),
	(r'^delete/$', 'uploader.publics.views.delete'),
	
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Example:
    # (r'^uploader/', include('uploader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)
