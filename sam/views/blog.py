from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Post, Tag, Comment, SiteImage
from django.db.models import Q
from sam.forms.tag_filter import TagFilterForm
from sam.forms.contact import ContactForm
from django.http import HttpResponseRedirect


def blog(request):
    posts = list(Post.objects.filter(private=False))
    if len(posts) > 5:
        posts = posts[len(posts) - 5:]
    posts.reverse()

    return render_to_response('blog.html', {
        "posts": posts,
    }, context_instance=RequestContext(request))


def post_archive(request):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        form = TagFilterForm()
        posts = list(Post.objects.filter(private=False))
        posts.reverse()
        archive = []
        for post in posts:
            archive.append({"month": post.creation_date.month, "year": post.creation_date.year})

        archive = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in archive)]
        archive.reverse()

    return render_to_response('blog_archive.html', {
        'archive': archive,
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

            if post_id and bot_test == '':
                comment = Comment.objects.create(private=private, name=name, email=email, subject=subject, message=message)
                post = Post.objects.get(pk=post_id)
                post.comments.add(comment)
            return HttpResponseRedirect('/blog/post/%s' % post_id)
    else:
        form = ContactForm()

    post = None
    exists = False
    images = []
    if post_id:
        post = Post.objects.filter(pk=post_id)
    if post:
        exists = True
        if post.filter(pk=post_id, private=False):
            post = post.get(pk=post_id, private=False)
            for image in post.images.values():
                images.append(SiteImage.objects.get(image=image['image']))
            images.reverse()

    return render_to_response('blog_post.html', {
        "post": post,
        "exists": exists,
        "images": images,
        "form": form,
    }, context_instance=RequestContext(request))


def filter(request, kind=None, tag=None):
    posts = None
    creation = None
    updated = None
    exists = False
    dates = []
    tags = []
    if request.method == 'POST':
        return filterHelp(request)
    else:
        if kind and tag:
            posts = Post.objects.all()

            if tag and '+' in tag and len(tag.split('+')) == 2:
                dates = tag.split('+')[0]
                dates = dates.split('*')
                tags = tag.split('+')[1]
                tags = tags.split('*')
            else:
                dates = None
                tags = tag.split('*')
            kinds = kind.split('+')

            if "date" in kinds:
                if not dates:
                    dates = tags
                if posts:
                    creation = posts
                    updated = posts
                    for piece in dates:
                        parts = piece.split('-')
                        if len(parts) == 3:
                            year = parts[2]
                            day = parts[1]
                            month = parts[0]
                            if num_or_all(year) and num_or_all(day) and num_or_all(month):
                                if not year == "all":
                                    creation = creation.filter(creation_date__year=int(year))
                                    updated = updated.filter(updated_date__year=int(year))
                                if not day == "all":
                                    creation = creation.filter(creation_date__day=int(day))
                                    updated = updated.filter(updated_date__day=int(day))
                                if not month == "all":
                                    creation = creation.filter(creation_date__month=int(month))
                                    updated = updated.filter(updated_date__month=int(month))
                            else:
                                posts = None
                        else:
                            posts = None
                    if (creation or updated) and posts:
                        exists = True

            if "tag" in kinds:
                if not "date" in kinds:
                    creation = posts
                    updated = posts
                if creation or updated:
                    for piece in tags:
                        creation = creation.filter(tags__tag=piece)
                        updated = updated.filter(tags__tag=piece)
                    if creation or updated:
                        exists = True
                    else:
                        exists = False

            if creation and updated and posts:
                creation = creation.filter(private=False)
                updated = updated.filter(private=False)
                posts = list(set(list(creation) + list(updated)))
                posts.reverse()

        form = TagFilterForm()

    return render_to_response('blog_filter.html', {
        'posts': posts,
        'exists': exists,
        'kind': kind,
        'tag': tag,
        'tags': tags,
        'dates': dates,
        'form': form,
    }, context_instance=RequestContext(request))


def num_or_all(x):
    if x == "all":
        return True
    try:
        int(x)
        return True
    except ValueError:
        return False


def filterHelp(request):
    form = TagFilterForm(request.POST)
    if form.is_valid():
        tag = form.cleaned_data['tag']
        date = form.cleaned_data['date']
        if not tag and not date:
            return HttpResponseRedirect('/blog/filter')
        elif not tag and date:
            return HttpResponseRedirect('/blog/filter/date/%s' % date)
        elif tag and not date:
            return HttpResponseRedirect('/blog/filter/tag/%s' % tag)
        elif tag and date:
            return HttpResponseRedirect('/blog/filter/date+tag/%s+%s' % (date, tag))
