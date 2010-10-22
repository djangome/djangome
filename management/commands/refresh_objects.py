import redis
import urllib
import operator
from django.conf import settings
from django.core.management.base import NoArgsCommand
from sphinx.ext import intersphinx
        
r = redis.Redis(**settings.REDIS)

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        
        # Parsing objects.inv is strange.
        urlpattern = 'http://docs.djangoproject.com/en/dev/%s'
        fp = urllib.urlopen(urlpattern % '_objects/')
        fp.readline()
        inv = intersphinx.read_inventory_v2(fp, urlpattern, operator.mod)
        
        # I'm entirelty not sure this is even close to correct.
        # There's a lot of info I'm throwing away here; revisit later?
        for keytype in inv:
            for term in inv[keytype]:
                _, _, url, _ = inv[keytype][term]
                self.save_term(term, url)
                if '.' in term:
                    self.save_term(term.split('.')[-1], url)

    def save_term(self, term, url):
        r.sadd('redirects:v1:%s' % term, url)
        r.setnx('redirects:v1:%s:%s' % (term, url), 1)
