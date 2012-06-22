from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'letsgetlouder.views.index_view'),
    url(r'^account/$', TemplateView.as_view(template_name='account.html')),
    url(r'^sign/$', 'letsgetlouder.views.sign_view'),
    url(r'^unsign/$', 'letsgetlouder.views.unsign_view'),
    url(r'^log-out/$', 'letsgetlouder.views.logout_view'),
    url(r'^buriedtreasure/', include(admin.site.urls)),
    url(r'', include('social_auth.urls'))
)
