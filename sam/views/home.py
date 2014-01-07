from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Quote, SiteImage
import random


def home(request):
    if Tag.objects.filter(tag="top_home"):
        posts = list(Post.objects.filter(tags__tag="top_home"))
        if posts:
            home_post = posts[-1]
            if home_post.image:
                banner_photo = home_post.image
            elif SiteImage.objects.filter(tags_tag="banner_photo"):
                banners = list(SiteImage.objects.filter(tags_tag="banner_photo"))
                banner_photo = banners[-1]
            else:
                banner_photo = None
        else:
            home_post = None
    else:
        home_post = None

    posts = list(Post.objects.filter(private=False))
    if posts:
        post = posts[-1]
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
        "quote": quote,
        "banner_photo": banner_photo
    }, context_instance=RequestContext(request))
