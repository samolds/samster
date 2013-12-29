from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Quote
import random
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.conf import settings

#@login_required
def home(request):
    if Tag.objects.filter(tag="home"):
        posts = list(Post.objects.filter(tags__tag="home"))
        posts.reverse()
        if posts:
            home_post = posts[0]
        else:
            home_post = None
    else:
        home_post = None

    posts = list(Post.objects.filter(private=False))
    posts.reverse()
    if posts:
        post = posts[0]
    else:
        post = None

    quotes = list(Quote.objects.filter(private=False))
    if quotes:
        quote = quotes[random.randrange(len(quotes))]
    else:
        quote = None

    #browser = request.META.get('HTTP_USER_AGENT', 'Unknown')
    return render_to_response('home.html', {
        "home_post": home_post,
        "post": post,
        "quote": quote
    }, context_instance=RequestContext(request))
