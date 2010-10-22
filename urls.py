from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^([\w-]+)$',       'djangome.views.redirect_to_term', name='redirect_to_term'),
    url('^([\w-]+)/stats$', 'djangome.views.show_term',        name='show_term'),
)
