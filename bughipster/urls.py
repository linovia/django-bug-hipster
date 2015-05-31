from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('bughipster.website.urls')),
    url(r'', include('bughipster.bz_admin.urls', namespace='back')),
    url(r'^admin/', include(admin.site.urls)),
]
