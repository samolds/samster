from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag
from sam.forms.blog_filter import BlogFilterForm
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
#from django.conf import settings

#@login_required
def blog(request):
    posts = list(Post.objects.filter(private=False))
    if len(posts) > 5:
        posts = posts[len(posts) - 5:]
    posts.reverse()
    return render_to_response('blog.html', {"posts": posts}, context_instance=RequestContext(request))


def all_posts(request):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        form = BlogFilterForm()
        posts = list(Post.objects.filter(private=False))
        posts.reverse()

    return render_to_response('blog_all.html', {
        'posts': posts,
        'form': form,
    }, context_instance=RequestContext(request))


def post(request, post_id=None):
    if post_id:
        exists = True
        if Post.objects.filter(pk=post_id):
            post = Post.objects.get(pk=post_id)
            if post.private:
              post = None
        else:
            post = None
            exists = False
    else:
        post = None
        exists = False
    return render_to_response('blog_post.html', {"post": post, "exists": exists}, context_instance=RequestContext(request))


def filter(request, tag=None):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        if tag:
            exists = True
            if Tag.objects.filter(tag=tag):
                tag_object = Tag.objects.filter(tag=tag)
                posts = list(Post.objects.filter(tags=tag_object, private=False))
                posts.reverse()
            else:
                posts = None
                exists = False
        else:
            posts = None
            exists = False

        form = BlogFilterForm()

    return render_to_response('blog_filter.html', {
        'posts': posts,
        'exists': exists,
        'tag': tag,
        'form': form,
    }, context_instance=RequestContext(request))


def filterHelp(request):
    form = BlogFilterForm(request.POST)
    if form.is_valid():
        tag = form.cleaned_data['tag']
        date = form.cleaned_data['date']


        # do a bunch of regex here


        if not tag and not date:
            return HttpResponseRedirect('/blog/all')
        elif not tag and date:
            return HttpResponseRedirect('/blog/filter/date%s' % date) # should be /blog/filter/tag/{{ tag }}
        elif tag and not date:
            return HttpResponseRedirect('/blog/filter/tag%s' % tag) # should be /blog/filter/date/{{ date }}
        elif tag and date:
            return HttpResponseRedirect('/blog/filter/tagdate%s%s' % (tag, date)) # should be /blog/filter/date/{{ date }}/tag/{{ tag }}
