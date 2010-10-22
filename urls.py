from django.conf.urls.defaults import *
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url('^$',               RedirectView.as_view(url='http://docs.djangoproject.com/en/dev/')),
    url('^t(?P<n>\d+)$',    RedirectView.as_view(url='http://code.djangoproject.com/ticket/%(n)s')),
    url('^r(?P<n>\d+)$',    RedirectView.as_view(url='http://code.djangoproject.com/changeset/%(n)s')),
    url('^([\w\-\.]+)$',       'djangome.views.redirect_to_term', name='redirect_to_term'),
    url('^([\w\-\.]+)/stats$', 'djangome.views.show_term',        name='show_term'),
)
