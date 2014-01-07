from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag


def about(request):
    post = None
    if Tag.objects.filter(tag="top_about"):
        posts = list(Post.objects.filter(tags__tag="top_about"))
        if posts:
            post = posts[-1]
    return render_to_response('about.html', {"post": post}, context_instance=RequestContext(request))
