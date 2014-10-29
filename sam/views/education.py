from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q


def education(request):
    education = cache.get("education")
    if not education:
        tag = Tag.objects.filter(tag="top_education")
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
        education = Q(tags__tag="education")
        school = Q(tags__tag="school")
        homework = Q(tags__tag="homework")

        posts = Post.objects.filter(education | school | homework)
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
        cache.set("education", cache_obj, settings.CACHE_LENGTH)
    else:
        post = education['post']
        posts = education['posts']
        images = education['images']
        full_post_stub = education['full_post_stub']

    return render_to_response('education.html', {
        "post": post,
        "posts": posts,
        "images": images,
        "full_post_stub": full_post_stub
    }, context_instance=RequestContext(request))
