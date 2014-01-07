from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Quote, SiteImage
import random


def home(request):
    home_post = None
    banner_photo = None
    if Tag.objects.filter(tag="top_home"):
        posts = list(Post.objects.filter(tags__tag="top_home"))
        if posts:
            home_post = posts[-1]
            if home_post.images.filter(tags__tag="banner_photo"):
                banners = list(home_post.images.filter(tags__tag="banner_photo"))
                banner_photo = banners[-1]
            elif SiteImage.objects.filter(tags__tag="banner_photo"):
                banners = list(SiteImage.objects.filter(tags__tag="banner_photo"))
                banner_photo = banners[-1]

    posts = list(Post.objects.filter(private=False))
    post = None
    if posts:
        post = posts[-1]

    quotes = list(Quote.objects.filter(private=False))
    quote = None
    if quotes:
        quote = quotes[random.randrange(len(quotes))]

    #browser = request.META.get('HTTP_USER_AGENT', 'Unknown')
    return render_to_response('home.html', {
        "home_post": home_post,
        "post": post,
        "quote": quote,
        "banner_photo": banner_photo
    }, context_instance=RequestContext(request))
