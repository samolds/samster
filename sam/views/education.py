from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post
from django.db.models import Q


def education(request):
    tag = Tag.objects.filter(tag="top_education")
    post = None
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        posts.reverse()
        post = posts[0]

    public = Q(private=False)
    education = Q(tags__tag="education")
    school = Q(tags__tag="school")
    homework = Q(tags__tag="homework")

    posts = Post.objects.filter(education | school | homework)
    posts = list(posts.filter(public))
    if len(posts) > 2:
        posts = posts[len(posts) - 2:]
    posts.reverse()

    return render_to_response('education.html', {
        "post": post,
        "posts": posts,
    }, context_instance=RequestContext(request))
