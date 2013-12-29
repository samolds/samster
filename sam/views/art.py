from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from sam.models import SiteImage, Tag, Comment
from django.db.models import Q
from sam.forms.tag_filter import TagFilterForm
from sam.forms.contact import ContactForm
from pytz import timezone, utc
from datetime import datetime
import re


def art(request):
    public = Q(private=False)
    art_tag = Q(tags__tag="art")
    drawing = Q(tags__tag="drawing")
    sketch = Q(tags__tag="sketch")
    photography = Q(tags__tag="photography")
    art = SiteImage.objects.filter(art_tag | drawing | sketch | photography)
    art = list(set(art.filter(public)))
    
    if len(art) > 5:
        art = art[len(art) - 5:]
    art.reverse()

    return render_to_response('art.html', {
        "art": art,
    }, context_instance=RequestContext(request))


def all_art(request):
    if request.method == 'POST':
        return filterHelp(request)
    else:
        public = Q(private=False)
        art_tag = Q(tags__tag="art")
        drawing = Q(tags__tag="drawing")
        sketch = Q(tags__tag="sketch")
        photography = Q(tags__tag="photography")
        art = SiteImage.objects.filter(art_tag | drawing | sketch | photography)
        art = list(set(art.filter(public)))
        art.reverse()
        form = TagFilterForm()

    return render_to_response('art_all.html', {
        'art': art,
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
            tags = tag.split('*')
            public = Q(private=False)
            art_tag = Q(tags__tag="art")
            drawing = Q(tags__tag="drawing")
            sketch = Q(tags__tag="sketch")
            photography = Q(tags__tag="photography")
            art = SiteImage.objects.filter(art_tag | drawing | sketch | photography)
            if kind == "tag":
                if art:
                    for piece in tags:
                        art = art.filter(tags__tag=piece)
                    if art:
                        exists = True
                        art = art.filter(public)
                    art = list(set(art))
                    art.reverse()
            elif kind == "date":
                dates = tags
                if art:
                    for piece in dates:
                        parts = piece.split('-')
                        if len(parts) == 3:
                            date = utc.localize(datetime(month=int(parts[0]), day=int(parts[1]), year=int(parts[2])))
                            creation_filter = Q(creation_date__month=date.month, creation_date__day=date.day, creation_date__year=date.year)
                            art = art.filter(creation_filter)
                        else:
                            art = None
                    if art:
                        exists = True
                        art = art.filter(public)
                        art = list(set(art))
                        art.reverse()
            elif kind == "date*tag":
                if tag and len(tag.split('_')) == 2:
                    dates = tag.split('_')[0]
                    dates = dates.split('*')
                    tags = tag.split('_')[1]
                    tags = tags.split('*')
                    if art:
                        for piece in dates:
                            parts = piece.split('-')
                            if len(parts) == 3:
                                date = utc.localize(datetime(month=int(parts[0]), day=int(parts[1]), year=int(parts[2])))
                                creation_filter = Q(creation_date__month=date.month, creation_date__day=date.day, creation_date__year=date.year)
                                art = art.filter(creation_filter)
                            else:
                                art = None
                        if art:
                            for piece in tags:
                                art = art.filter(tags__tag=piece)
                            if art:
                                exists = True
                                art = art.filter(public)
                                art = list(set(art))
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


def filterHelp(request):
    form = TagFilterForm(request.POST)
    if form.is_valid():
        tag = form.cleaned_data['tag']
        date = form.cleaned_data['date']
        if not tag and not date:
            return HttpResponseRedirect('/art/all')
        elif not tag and date:
            return HttpResponseRedirect('/art/filter/date/%s' % date)
        elif tag and not date:
            return HttpResponseRedirect('/art/filter/tag/%s' % tag)
        elif tag and date:
            return HttpResponseRedirect('/art/filter/date*tag/%s_%s' % (date, tag))
