from sam.models import Post, Tag, Quote, SiteImage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
import random


def home(request):
    public = Q(private=False)
    home_post = None
    home_images = []
    if SiteImage.objects.filter(tags__tag="banner_photo").filter(public):
        banners = list(SiteImage.objects.filter(tags__tag="banner_photo").filter(public))
        banner_photo = banners[-1]
    else:
        banner_photo = None
    if Tag.objects.filter(tag="top_home"):
        posts = list(Post.objects.filter(tags__tag="top_home"))
        if posts:
            home_post = posts[-1]
            if home_post.images.filter(tags__tag="banner_photo").filter(public):
                banners = list(home_post.images.filter(tags__tag="banner_photo").filter(public))
                banner_photo = banners[-1]
            for image in home_post.images.values():
                home_images.append(SiteImage.objects.get(image=image['image']))
            home_images.reverse()

    posts = list(Post.objects.filter(public).exclude(tags__tag__startswith="top_"))

    art_tag = Q(tags__tag="art")
    drawing = Q(tags__tag="drawing")
    photography = Q(tags__tag="photography")
    art_image = SiteImage.objects.filter(art_tag | drawing | photography)

    art_image = list(set(art_image.filter(public)))

    posts = art_image + posts
    posts.sort(key=lambda x: x.creation_date)

    post = None
    images = []
    is_site_image = True
    if posts:
        post = posts[-1]
        if type(post) == Post:
            is_site_image = False
            for image in post.images.values():
                images.append(SiteImage.objects.get(image=image['image']))
            images.reverse()

    full_post_stub = False

    quotes = list(Quote.objects.filter(public).filter(length__lt = 200))
    quote = None
    if quotes:
        quote = quotes[random.randrange(len(quotes))]

    return render_to_response('home.html', {
        "home_post": home_post,
        "home_images": home_images,
        "post": post,
        "images": images,
        "is_site_image": is_site_image,
        "quote": quote,
        "banner_photo": banner_photo,
        "full_post_stub": full_post_stub
    }, context_instance=RequestContext(request))
