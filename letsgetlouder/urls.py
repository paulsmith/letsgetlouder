from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from .views import LoginRedirect, LoginCallback


urlpatterns = patterns('',
    url(r'^$', 'letsgetlouder.views.index_view'),
    url(r'^account/$', TemplateView.as_view(template_name='account.html')),
    url(r'^sign/$', 'pledge.views.sign_view', name='sign-pledge'),
    url(r'^unsign/$', 'pledge.views.unsign_view', name='unsign-pledge'),
    url(r'^log-out/$', 'letsgetlouder.views.logout_view'),
    url(r'^buriedtreasure/', include(admin.site.urls)),
    url(r'^login/(?P<provider>(\w|-)+)/$', LoginRedirect.as_view(), name='login'),
    url(r'^callback/(?P<provider>(\w|-)+)/$', LoginCallback.as_view(), name='login-callback'),
)
