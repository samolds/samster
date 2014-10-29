from django.shortcuts import render_to_response
from sam.models import Post, Tag, SiteImage
from django.template import RequestContext
from django.core.cache import cache


def about(request):
    about = cache.get("about")
    if not about:
        post = None
        images = []
        if Tag.objects.filter(tag="top_about"):
            posts = list(Post.objects.filter(tags__tag="top_about"))
            if posts:
                post = posts[-1]
                for image in post.images.values():
                    images.append(SiteImage.objects.get(image=image['image']))
                images.reverse()

        cache_obj = {
            "post": post,
            "images": images,
        }
        cache.set("about", cache_obj)
    else:
        post = about['post']
        images = about['images']

    return render_to_response('about.html', {
      "post": post,
      "images": images,
    }, context_instance=RequestContext(request))
