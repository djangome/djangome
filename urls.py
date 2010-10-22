from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url('^$',               redirect_to, {'url': 'http://docs.djangoproject.com/en/dev/'}),
    url('^([\w-]+)$',       'djangome.views.redirect_to_term', name='redirect_to_term'),
    url('^([\w-]+)/stats$', 'djangome.views.show_term',        name='show_term'),
)
