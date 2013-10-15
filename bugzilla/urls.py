from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'bugzilla.views.home', name='home'),
    # url(r'^bugzilla/', include('bugzilla.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
