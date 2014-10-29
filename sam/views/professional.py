from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.core.cache import cache
from django.db.models import Q


def professional(request):
    professional = cache.get("professional")
    if not professional:
        tag = Tag.objects.filter(tag="top_professional")
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
        professional = Q(tags__tag="professional")
        work = Q(tags__tag="work")
        job = Q(tags__tag="job")

        posts = Post.objects.filter(professional | work | job)
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
        cache.set("professional", cache_obj)
    else:
        post = professional['post']
        posts = professional['posts']
        images = professional['images']
        full_post_stub = professional['full_post_stub']
        

    return render_to_response('professional.html', {
        "post": post,
        "posts": posts,
        "images": images,
        "full_post_stub": full_post_stub
    }, context_instance=RequestContext(request))
