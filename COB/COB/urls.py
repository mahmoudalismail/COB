from django.conf.urls import patterns, include, url
from COBApp import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'COB.views.home', name='home'),
    # url(r'^COB/', include('COB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^COBApp/', include('COBApp.urls'))
)

# fixing the admin page 
from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))