from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Comment
from sam.forms.blog_filter import BlogFilterForm
from sam.forms.contact import ContactForm
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from pytz import timezone
from datetime import datetime
import re
#from django.conf import settings

#@login_required
def blog(request):
    posts = list(Post.objects.filter(private=False))
    if len(posts) > 5:
        posts = posts[len(posts) - 5:]
    posts.reverse()

    return render_to_response('blog.html', {
        "posts": posts,
    }, context_instance=RequestContext(request))


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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            private = form.cleaned_data['private']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bot_test = form.cleaned_data['email_confirmation']

            if post_id:
                comment = Comment.objects.create(private=private, name=name, email=email, subject=subject, message=message)
                post = Post.objects.get(pk=post_id)
                post.comments.add(comment)
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
    form = ContactForm()

    return render_to_response('blog_post.html', {
        "post": post,
        "exists": exists,
        "form": form,
    }, context_instance=RequestContext(request))


def filter(request, kind=None, tag=None):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        if kind and tag:
            exists = True
            tags = tag.split('*')
            posts = Post.objects.filter(private=False)
            if kind == "tag":
                if posts:
                    for piece in tags:
                        posts = posts.filter(tags__tag=piece)
                    posts = list(posts.reverse())
                else:
                    posts = None
                    exists = False
            elif kind == "date":
                utc = timezone('UTC').localize
                if posts:
                    postscd = posts
                    postsud = posts
                    for piece in tags:
                        parts = piece.split('-')
                        date = utc(datetime(month=int(parts[0]), day=int(parts[1]), year=int(parts[2])))
                        # import pdb; pdb.set_trace()
                        postscd = postscd.filter(creation_date__month=date.month).filter(creation_date__day=date.day).filter(creation_date__year=date.year)
                        postsud = postsud.filter(updated_date__month=date.month).filter(updated_date__day=date.day).filter(updated_date__year=date.year)
                    posts = list(postscd) + list(postsud)
                    posts = posts.reverse()
                else:
                    posts = None
                    exists = False
            elif kind == "date*tag":
                dates = tag.split('_')[0]
                dates = dates.split('*')
                tags = tag.split('_')[1]
                tags = tags.split('*')
                if posts:
                    for piece in dates:
                        posts = posts.filter(tags__tag=piece)
                    for piece in tags:
                        posts = posts.filter(tags__tag=piece)
                    posts = list(posts.reverse())
                else:
                    posts = None
                    exists = False
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
        'kind': kind,
        'tag': tag,
        'form': form,
    }, context_instance=RequestContext(request))


def filterHelp(request):
    form = BlogFilterForm(request.POST)
    if form.is_valid():
        tag = form.cleaned_data['tag']
        date = form.cleaned_data['date']
        if not tag and not date:
            return HttpResponseRedirect('/blog/all')
        elif not tag and date:
            # regex stuff for date
            return HttpResponseRedirect('/blog/filter/date/%s' % date) # should be /blog/filter/tag/{{ tag }}
        elif tag and not date:
            # regex stuff for tags
            return HttpResponseRedirect('/blog/filter/tag/%s' % tag) # should be /blog/filter/date/{{ date }}
        elif tag and date:
            # regex stuff for both
            return HttpResponseRedirect('/blog/filter/date*tag/%s_%s' % (tag, date)) # should be /blog/filter/date/{{ date }}/tag/{{ tag }}
