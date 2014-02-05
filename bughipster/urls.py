from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'bughipster.views.home', name='home'),
    # url(r'^bughipster/', include('bughipster.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
