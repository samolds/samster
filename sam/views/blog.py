from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.conf import settings

#@login_required
def blog(request):
    posts = Post.objects.all()
    if len(posts) > 5:
        posts = posts[len(posts) - 5:]
    posts.reverse()
    return render_to_response('blog.html', {"posts": posts}, context_instance=RequestContext(request))


def all_posts(request):
    posts = list(Post.objects.all())
    posts.reverse()
    return render_to_response('blog_all.html', {"posts": posts}, context_instance=RequestContext(request))


def post(request, post_id=None):
    if post_id:
        exists = True
        if Post.objects.filter(pk=post_id):
            post = Post.objects.get(pk=post_id)
        else:
            post = None
            exists = False
    else:
        post = None
        exists = False
    return render_to_response('blog_post.html', {"post": post, "exists": exists}, context_instance=RequestContext(request))


def filter(request, tag=None):
    if tag:
        exists = True
        if Tag.objects.filter(tag=tag):
            tag_object = Tag.objects.filter(tag=tag)
            posts = list(Post.objects.filter(tags=tag_object))
            posts.reverse()
        else:
            posts = None
            exists = False
    else:
        posts = None
        exists = False
    return render_to_response('blog_filter.html', {"posts": posts, "exists": exists, "tag": tag}, context_instance=RequestContext(request))
