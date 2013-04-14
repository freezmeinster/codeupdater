from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^source-code-update/$', 'updater.code_update.views.index', name='index'),
     url(r'^source-code-update/mulai$', 'updater.code_update.views.mulai', name='mulai'),
     url(r'^source-code-update/status$', 'updater.code_update.views.status', name='status'),
    # url(r'^updater/', include('updater.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
