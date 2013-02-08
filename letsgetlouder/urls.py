from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from .views import LoginRedirect, LoginCallback


urlpatterns = patterns('',
    url(r'^$', 'letsgetlouder.views.index_view'),
    url(r'^account/$', TemplateView.as_view(template_name='account.html'), name="account"),
    url(r'^sign/$', 'pledge.views.sign_view', name='sign-pledge'),
    url(r'^unsign/$', 'pledge.views.unsign_view', name='unsign-pledge'),
    url(r'^log-out/$', 'letsgetlouder.views.logout_view'),
    url(r'^buriedtreasure/', include(admin.site.urls)),
    url(r'^login/(?P<provider>(\w|-)+)/$', LoginRedirect.as_view(), name='login'),
    url(r'^callback/(?P<provider>(\w|-)+)/$', LoginCallback.as_view(), name='login-callback'),
)

if getattr(settings, 'HEROKU', False):
    # Heroku won't serve static files by default
    # https://github.com/heroku/heroku-buildpack-python/issues/32
    # Gunicorn with an async worker (Gevent) can handle this just fine for the
    # expected load.
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': False, }),
    )
