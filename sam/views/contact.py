from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.forms.contact import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from sam.models import Post, Tag, Comment


def contact(request):
    tag = Tag.objects.filter(tag="contact")
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        posts.reverse()
        post = posts[0]
    else:
        post = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            private = form.cleaned_data['private']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bot_test = form.cleaned_data['email_confirmation']

            comment = Comment.objects.create(private=private, name=name, email=email, subject=subject, message=message)
            if post:
                post.comments.add(comment)

            email_message = "%s \n\n - %s (%s)" % (message, name, email)

            if bot_test == '':
                try:
                    #import pdb; pdb.set_trace()
                    send_mail(subject, email_message, email, settings.CONTACT_EMAIL_RECIPIENT)
                except Exception as e:
                    print e
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {
        'form': form,
        'post': post,
    }, context_instance=RequestContext(request))
