from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic import RedirectView

ALL_VERSIONS_RE = '(?P<version>%s)' % '|'.join(settings.DJANGOME['VERSIONS'])

urlpatterns = patterns('',
    url('^$',
        RedirectView.as_view(url='http://docs.djangoproject.com/en/dev/')
    ),
    url('^t(?P<n>\d+)$',
        RedirectView.as_view(url='http://code.djangoproject.com/ticket/%(n)s')
    ),
    url('^r(?P<n>\d+)$',
        RedirectView.as_view(url='http://code.djangoproject.com/changeset/%(n)s')
    ),
    url('^__oneoffs__$',
        'djangome.views.manage_oneoffs',
        name = "manage_oneoffs",
    ),
    url('^(?P<term>[\w\-\.]+)$',
        'djangome.views.redirect_to_term',
        {'version': settings.DJANGOME['DEFAULT_VERSION']},
    ),
    url('^(?P<term>[\w\-\.]+)/stats$',
        'djangome.views.show_term',
        {'version': settings.DJANGOME['DEFAULT_VERSION']},
    ),
    url('^%s/(?P<term>[\w\-\.]+)$' % ALL_VERSIONS_RE,
        'djangome.views.redirect_to_term',
        name = 'redirect_to_term'
    ),
    url('^%s/(?P<term>[\w\-\.]+)/stats$' % ALL_VERSIONS_RE,
        'djangome.views.show_term',
        name = 'show_term'
    ),
)
