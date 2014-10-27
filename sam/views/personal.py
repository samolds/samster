from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.db.models import Q


def personal(request):
    tag = Tag.objects.filter(tag="top_personal")
    post = None
    images = []
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        if posts:
            post = posts[-1]
            for image in post.images.values():
                images.append(SiteImage.objects.get(image=image['image']))
            images.reverse()

    public = Q(private=False)
    personal = Q(tags__tag="personal")
    thoughts = Q(tags__tag="thoughts")
    shower_thoughts = Q(tags__tag="shower_thoughts")

    posts = Post.objects.filter(personal | thoughts | shower_thoughts)
    posts = list(set(posts.filter(public)))

    if len(posts) > 2:
        posts = posts[len(posts) - 2:]
    posts.reverse()

    return render_to_response('personal.html', {
        "post": post,
        "posts": posts,
        "images": images,
    }, context_instance=RequestContext(request))
