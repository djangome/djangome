import redis
import urllib
import operator
from django.conf import settings
from django.core.management.base import NoArgsCommand
from sphinx.ext import intersphinx
        
r = redis.Redis(**settings.REDIS)

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        v1_keys = r.keys('redirects:v1:*')
        for k in v1_keys:
            if r.type(k) == 'set':
                term = k.rsplit(':')[-1]
                for url in r.smembers(k):
                    score = r.get('redirects:v1:%s:%s' % (term, url))
                    r.sadd('redirects:v2:dev:%s' % (term,), url)
                    r.set('redirects:v2:dev:%s:%s' % (term, url), score)