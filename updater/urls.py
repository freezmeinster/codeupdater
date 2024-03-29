from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^source-code-update/login$', 'updater.code_update.views.login_page', name='login'),
     url(r'^source-code-update/logout$', 'updater.code_update.views.logout_page', name='logout'),
     url(r'^source-code-update/$', 'updater.code_update.views.index', name='index'),
     url(r'^source-code-update/mulai$', 'updater.code_update.views.mulai', name='mulai'),
     url(r'^source-code-update/mulai-db$', 'updater.code_update.views.mulai_db', name='mulai_db'),
     url(r'^source-code-update/mulai-clean$', 'updater.code_update.views.mulai_clean', name='mulai_clean'),
     url(r'^source-code-update/status$', 'updater.code_update.views.status', name='status'),
     url(r'^source-code-update/status-db$', 'updater.code_update.views.status_db', name='status_db'),
     url(r'^source-code-update/status-clean$', 'updater.code_update.views.status_clean', name='status_clean'),
)
