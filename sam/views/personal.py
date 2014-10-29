from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q


def personal(request):
    personal = cache.get("personal")
    if not personal:
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
        full_post_stub = False

        cache_obj = {
            "post": post,
            "posts": posts,
            "images": images,
            "full_post_stub": full_post_stub
        }
        cache.set("personal", cache_obj, settings.CACHE_LENGTH)
    else:
        post = personal['post']
        posts = personal['posts']
        images = personal['images']
        full_post_stub = personal['full_post_stub']

    return render_to_response('personal.html', {
        "post": post,
        "posts": posts,
        "images": images,
        "full_post_stub": full_post_stub
    }, context_instance=RequestContext(request))
