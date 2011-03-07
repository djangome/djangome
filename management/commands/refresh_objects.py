import redis
import urllib
import operator
from django.conf import settings
from django.core.management.base import NoArgsCommand
from sphinx.ext import intersphinx
        
r = redis.Redis(**settings.REDIS)

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for version in settings.DJANGOME['VERSIONS']:
            self.refresh_version(version)
            
    def refresh_version(self, version):
        inv = self.parse_sphinx_inventory(version)
        
        # I'm entirelty not sure this is even close to correct.
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
