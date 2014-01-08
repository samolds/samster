from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, SiteImage


def about(request):
    post = None
    images = []
    if Tag.objects.filter(tag="top_about"):
        posts = list(Post.objects.filter(tags__tag="top_about"))
        if posts:
            post = posts[-1]
            for image in post.images.values():
                images.append(SiteImage.objects.get(image=image['image']))
            images.reverse()

    return render_to_response('about.html', {
      "post": post,
      "images": images,
    }, context_instance=RequestContext(request))
