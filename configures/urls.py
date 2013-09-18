from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^services/(?P<handler>[a-zA-Z]+)/(?P<service>[a-zA-Z]+)[/]?$","ou_fyp.views.handleRequest",{"invokeType":"services"}),
    url(r"^(?P<handler>[a-zA-Z]+)/(?P<service>[a-zA-Z]+)[/]?$","ou_fyp.views.handleRequest",{"invokeType":"templates"}),
    url(r"^services/project/load/(?P<pId>[0-9]+)/(?P<version>[0-9]+)[/]?$","ou_fyp.views.loadSTL"),
    url(r"^project/panel/(?P<pId>[0-9]+)/(?P<version>[0-9]+)[/]?$","ou_fyp.views.panel"),
    # Examples:
    # url(r'^$', 'configures.views.home', name='home'),
    # url(r'^configures/', include('configures.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
