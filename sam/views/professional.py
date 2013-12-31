from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post
from django.db.models import Q


def professional(request):
    tag = Tag.objects.filter(tag="top_professional")
    post = None
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        posts.reverse()
        post = posts[0]

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
    }, context_instance=RequestContext(request))
