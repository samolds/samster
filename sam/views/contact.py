from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.forms.contact import ContactForm
from django.core.cache import cache
from sam.models import Post, Tag, Comment, SiteImage


def contact(request):
    contact = cache.get("contact")
    if not contact:
        tag = Tag.objects.filter(tag="top_contact")
        post = None
        images = []
        if tag:
            posts = list(Post.objects.filter(tags=tag))
            if posts:
                post = posts[-1]
                for image in post.images.values():
                    images.append(SiteImage.objects.get(image=image['image']))
                images.reverse()

        cache_obj = {
            'post': post,
            "images": images,
        }
        cache.set("contact", cache_obj)
    else:
        post = contact['post']
        images = contact['images']

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            private = form.cleaned_data['private']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bot_test = form.cleaned_data['email_confirmation']

            if bot_test == '':
                comment = Comment.objects.create(private=private, name=name, email=email, subject=subject, message=message)
                if post:
                    post.comments.add(comment)
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {
        'form': form,
        'post': post,
        "images": images,
    }, context_instance=RequestContext(request))
