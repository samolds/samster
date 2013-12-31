from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.conf import settings

#@login_required
def about(request):
    if Tag.objects.filter(tag="top_about"):
        posts = list(Post.objects.filter(tags__tag="top_about"))
        posts.reverse()
        if posts:
            post = posts[0]
        else:
            post = None
    else:
        post = None
    return render_to_response('about.html', {"post": post}, context_instance=RequestContext(request))
