import redis
import itertools
import operator
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.conf import settings
from django.shortcuts import render_to_response as render
from django.shortcuts import redirect

r = redis.Redis(**settings.REDIS)

class RedirectForm(forms.Form):
    _prefix = 'http://docs.djangoproject.com/en/dev/'     
    url = forms.URLField(label='URL', initial=_prefix)
    
    def clean_url(self):
        url = self.cleaned_data['url']
        if url.startswith(self._prefix) and url != self._prefix:
            return url
        raise forms.ValidationError('Please enter a valid URL starting with %s' % self._prefix)

def redirect_to_term(request, term):
    form = RedirectForm(request.GET or None)

    # If we're explicitly choosing a new URL for this term, just go ahead and
    # do that. This could also insert new URLs, so do a brief sanity check to
    # make sure this service can't be used for spam.
    if 'url' in request.GET:
        if form.is_valid():
            # Make sure the new URL is in the set of URLs and increment its score.
            url = form.cleaned_data['url']
            r.sadd('redirects:v1:%s' % term, url)
            r.incr('redirects:v1:%s:%s' % (term, url))
            return redirect(request.GET.get('return_to', url))
    
    urls = get_urls(term)
    if urls:
        scoregroups = group_urls(urls)
    
        # The first group is the URLs with the highest score.
        score, winners = scoregroups.next()
    
        # If there's only a single winning URL, we're done. Count the redirect and
        # then issue it.
        if len(winners) == 1:
            url = winners[0]
            r.incr('redirects:v1:%s:%s' % (term, url))
            return redirect(url)

        # Otherwise we need to display a list of all choices. We'll present this into
        # two buckets: the tied URLs with the high score (which is the list of winners
        # we've already gotten) and the tied URLs with a lower score. This second
        # bucket might be empty.
        losers = [losing_group for score, losing_group in scoregroups]
    
    else:
        winners = losers = None
    
    return render('choices.html', {
        'term': term,
        'winners': winners,
        'losers': losers,
        'form': form
    })

def show_term(request, term):
    return render('show.html', {
        'term': term,
        'urls': get_urls(term),
        'can_edit': True,
    })
    
def get_urls(term):
    """
    Gets the set of URLs for <term>.
    
    Returns a list of (score, url) tuples, sorted by score descending.
    """
    # Sort the set of URLs in redirects:v1:term by the scores (clicks) in
    # redirects:v1:term:url, then get each score along with each URL.
    # This returns a list [score, url, score, url, ...]
    urls = r.sort('redirects:v1:%s' % term, 
                  by   = 'redirects:v1:%s:*' % term, 
                  get  = ('redirects:v1:%s:*' % term, '#'),
                  desc = True)

    # Convert that to a list of tuples [(score, url), (score, url), ...]
    return zip(urls[::2], urls[1::2])
    
def group_urls(urls):
    """
    Given a list of (score, url) tuples, group them into buckets by score.
    
    Returns a list of (score, list_of_urls) tuples.
    """
    for (score, group) in itertools.groupby(urls, operator.itemgetter(0)):
        yield (score, [url for score, url in group])