from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from sam.models import SiteImage, Tag, Comment, Post
from django.db.models import Q
from sam.forms.tag_filter import TagFilterForm
from sam.forms.contact import ContactForm


def art(request):
    public = Q(private=False)
    art_tag = Q(tags__tag="art")
    drawing = Q(tags__tag="drawing")
    photography = Q(tags__tag="photography")
    art_image = SiteImage.objects.filter(art_tag | drawing | photography)
    art_post = Post.objects.filter(art_tag | drawing | photography)

    art_image = list(set(art_image.filter(public)))
    art_post = list(set(art_post.filter(public)))

    art = art_image + art_post
    art.sort(key=lambda x: x.creation_date)

    if len(art) > 5:
        art = art[len(art) - 5:]
    art.reverse()

    return render_to_response('art.html', {
        "art": art,
    }, context_instance=RequestContext(request))


def art_archive(request):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        form = TagFilterForm()
        public = Q(private=False)
        art_tag = Q(tags__tag="art")
        drawing = Q(tags__tag="drawing")
        photography = Q(tags__tag="photography")
        art_image = SiteImage.objects.filter(art_tag | drawing | photography)
        art_post = Post.objects.filter(art_tag | drawing | photography)

        art_image = list(set(art_image.filter(public)))
        art_post = list(set(art_post.filter(public)))

        art = art_image + art_post
        art.sort(key=lambda x: x.creation_date)

        art.reverse()

        archive = []
        for work in art:
            archive.append({"month": work.creation_date.month, "year": work.creation_date.year})

        archive = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in archive)]
        archive.reverse()

    return render_to_response('art_archive.html', {
        'archive': archive,
        'form': form,
    }, context_instance=RequestContext(request))


def art_work(request, image_id=None):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            private = form.cleaned_data['private']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bot_test = form.cleaned_data['email_confirmation']

            if image_id and bot_test == '':
                comment = Comment.objects.create(private=private, name=name, email=email, subject=subject, message=message)
                image = SiteImage.objects.get(pk=image_id)
                image.comments.add(comment)
            return HttpResponseRedirect('/art/work/%s' % image_id)
    else:
        form = ContactForm()

    work = None
    exists = False
    if image_id:
        work = SiteImage.objects.filter(pk=image_id)
    if work:
        exists = True
        if work.filter(pk=image_id, private=False):
            work = work.get(pk=image_id, private=False)
        else:
            work = None

    return render_to_response('art_work.html', {
        "work": work,
        "exists": exists,
        "form": form,
    }, context_instance=RequestContext(request))


def filter(request, kind=None, tag=None):
    art = None
    exists = False
    dates = []
    tags = []
    if request.method == 'POST':
        return filterHelp(request)
    else:
        if kind and tag:
            public = Q(private=False)
            art_tag = Q(tags__tag="art")
            drawing = Q(tags__tag="drawing")
            photography = Q(tags__tag="photography")

            art_image = SiteImage.objects.filter(art_tag | drawing | photography)
            art_post = Post.objects.filter(art_tag | drawing | photography)

            if tag and "+" in tag and len(tag.split('+')) == 2:
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
                if art_image or art_post:
                    good_request = True
                    for piece in dates:
                        parts = piece.split('-')
                        if len(parts) == 3:
                            year = parts[2]
                            day = parts[1]
                            month = parts[0]
                            if num_or_all(year) and num_or_all(day) and num_or_all(month):
                                if not year == "all":
                                    art_image = art_image.filter(creation_date__year=int(year))
                                    art_post = art_post.filter(creation_date__year=int(year))
                                if not day == "all":
                                    art_image = art_image.filter(creation_date__day=int(day))
                                    art_post = art_post.filter(creation_date__day=int(day))
                                if not month == "all":
                                    art_image = art_image.filter(creation_date__month=int(month))
                                    art_post = art_post.filter(creation_date__month=int(month))
                            else:
                                good_request = False
                        else:
                            good_request = False
                    if (art_image or art_post) and good_request:
                        exists = True

            if "tag" in kinds:
                if art_image or art_post:
                    for piece in tags:
                        art_image = art_image.filter(tags__tag=piece)
                        art_post = art_post.filter(tags__tag=piece)
                    if art_image or art_post:
                        exists = True
                    else:
                        exists = False

            art_image = art_image.filter(public)
            art_post = art_post.filter(public)
            art_image = list(set(art_image))
            art_post = list(set(art_post))
            art = art_image + art_post
            art.sort(key=lambda x: x.creation_date)
            art.reverse()

        form = TagFilterForm()

    return render_to_response('art_filter.html', {
        'art': art,
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
            return HttpResponseRedirect('/art/filter')
        elif not tag and date:
            return HttpResponseRedirect('/art/filter/date/%s' % date)
        elif tag and not date:
            return HttpResponseRedirect('/art/filter/tag/%s' % tag)
        elif tag and date:
            return HttpResponseRedirect('/art/filter/date+tag/%s+%s' % (date, tag))
