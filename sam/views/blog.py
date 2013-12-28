from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Comment
from sam.forms.blog_filter import BlogFilterForm
from sam.forms.contact import ContactForm
from django.http import HttpResponseRedirect
from pytz import timezone, utc
from datetime import datetime
from django.db.models import Q
import re


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
    else:
        form = ContactForm()

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

    return render_to_response('blog_post.html', {
        "post": post,
        "exists": exists,
        "form": form,
    }, context_instance=RequestContext(request))


def filter(request, kind=None, tag=None):
    posts = None
    exists = False
    dates = []
    tags = []
    if request.method == 'POST':
        return filterHelp(request)
    else:
        if kind and tag:
            tags = tag.split('*')
            posts = Post.objects.all()
            if kind == "tag":
                if posts:
                    for piece in tags:
                        posts = posts.filter(tags__tag=piece)
                    if posts:
                        exists = True
                        posts = posts.filter(private=False)
                    posts = list(posts)
                    posts.reverse()
            elif kind == "date":
                if posts:
                    temp = posts
                    dates = tags
                    for piece in dates:
                        parts = piece.split('-')
                        if len(parts) == 3:
                            date = utc.localize(datetime(month=int(parts[0]), day=int(parts[1]), year=int(parts[2])))
                            creation_filter = Q(creation_date__month=date.month, creation_date__day=date.day, creation_date__year=date.year)
                            updated_filter = Q(updated_date__month=date.month, updated_date__day=date.day, updated_date__year=date.year)
                            temp = temp.filter(creation_filter | updated_filter)
                        else:
                            temp = None
                    if temp:
                        exists = True
                        temp = temp.filter(private=False)
                        posts = list(set(temp))
                        posts.reverse()
                    else:
                        posts = temp
            elif kind == "date*tag":
                if tag and len(tag.split('_')) == 2:
                    dates = tag.split('_')[0]
                    dates = dates.split('*')
                    tags = tag.split('_')[1]
                    tags = tags.split('*')
                    if posts:
                        for piece in dates:
                            parts = piece.split('-')
                            if len(parts) == 3:
                                date = utc.localize(datetime(month=int(parts[0]), day=int(parts[1]), year=int(parts[2])))
                                creation_filter = Q(creation_date__month=date.month, creation_date__day=date.day, creation_date__year=date.year)
                                updated_filter = Q(updated_date__month=date.month, updated_date__day=date.day, updated_date__year=date.year)
                                posts = posts.filter(creation_filter | updated_filter)
                            else:
                                posts = None
                        if posts:
                            for piece in tags:
                                posts = posts.filter(tags__tag=piece)
                            if posts:
                                exists = True
                                posts = posts.filter(private=False)
                                posts = list(set(posts))
                                posts.reverse()

        form = BlogFilterForm()

    return render_to_response('blog_filter.html', {
        'posts': posts,
        'exists': exists,
        'kind': kind,
        'tag': tag,
        'tags': tags,
        'dates': dates,
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
            return HttpResponseRedirect('/blog/filter/date/%s' % date)
        elif tag and not date:
            return HttpResponseRedirect('/blog/filter/tag/%s' % tag)
        elif tag and date:
            return HttpResponseRedirect('/blog/filter/date*tag/%s_%s' % (date, tag))
