http://django.me/<term> -- redirect to the most appropriate doc page for <term>.

Data model:

    redirects:v2:{version}:{term}
        -> a set of all URLs for {term} in version {version}
           e.g.: redirects:v2:1.6:ModelForm

    redirects:v2:{version}:{term}:{url}
        -> the count of hits for {term} that redirected to {url}

    redirects:v2:titles:{url}
        -> the title of {url}

Running locally:

- Install the Heroku toolbelt (to get Forman).
- Edit .env if apropriate (to update the redis info, probably).
- foreman start

Running on Heroku:

    $ heroku addons:add securekey
    $ heroku addons:add rediscloud
    $ heroku config:set ALLOWED_HOSTS=yourapp.herokuapp.com
    $ git push heroku master
