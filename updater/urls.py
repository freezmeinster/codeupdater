from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^source-code-update/$', 'updater.code_update.views.index', name='index'),
     url(r'^source-code-update/mulai$', 'updater.code_update.views.mulai', name='mulai'),
     url(r'^source-code-update/mulai-db$', 'updater.code_update.views.mulai_db', name='mulai_db'),
     url(r'^source-code-update/status$', 'updater.code_update.views.status', name='status'),
     url(r'^source-code-update/status-db$', 'updater.code_update.views.status_db', name='status_db'),

)
