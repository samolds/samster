from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.forms.contact import ContactForm
from sam.models import Post, Tag, Comment


def contact(request):
    tag = Tag.objects.filter(tag="top_contact")
    post = None
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        if posts:
            post = posts[-1]

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
    }, context_instance=RequestContext(request))
