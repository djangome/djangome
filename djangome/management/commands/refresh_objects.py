from __future__ import print_function

import redis
import urllib
import operator
from django.conf import settings
from django.core.management.base import NoArgsCommand
from sphinx.ext import intersphinx

r = redis.StrictRedis.from_url(settings.REDIS_URL)

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for version in settings.DJANGOME['VERSIONS']:
            print('Refreshing', version)
            termcount = self.refresh_version(version)
            print(termcount, 'terms')

    def refresh_version(self, version):
        termcount = 0
        inv = self.parse_sphinx_inventory(version)

        # I'm entirely not sure this is even close to correct.
        # There's a lot of info I'm throwing away here; revisit later?
        for keytype in inv:
            for term in inv[keytype]:
                _, _, url, title = inv[keytype][term]
                if not title or title == '-':
                    if '#' in url:
                        title = url.rsplit('#')[-1]
                    else:
                        title = url
                self.save_term(version, term, url, title)
                if '.' in term:
                    self.save_term(version, term.split('.')[-1], url, title)
                    termcount += 1

        return termcount

    def parse_sphinx_inventory(self, version):
        # Parsing objects.inv is strange.
        urlpattern = 'http://docs.djangoproject.com/en/%s/%%s' % version
        fp = urllib.urlopen(urlpattern % '_objects/')
        fp.readline()
        return intersphinx.read_inventory_v2(fp, urlpattern, operator.mod)

    def save_term(self, version, term, url, title):
        r.sadd('redirects:v2:%s:%s' % (version, term), url)
        r.setnx('redirects:v2:%s:%s:%s' % (version, term, url), 1)
        r.set('redirects:v2:titles:%s' % (url,), title)
