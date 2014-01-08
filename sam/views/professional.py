from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.db.models import Q


def professional(request):
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
    posts = list(posts.filter(public))
    if len(posts) > 2:
        posts = posts[len(posts) - 2:]
    posts.reverse()

    return render_to_response('professional.html', {
        "post": post,
        "posts": posts,
        "images": images,
    }, context_instance=RequestContext(request))
