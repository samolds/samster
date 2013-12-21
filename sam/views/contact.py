from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.forms.contact import ContactForm
from django.conf import settings
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bot_test = form.cleaned_data['email_confirmation']


            email_message = "%s \n\n - %s (%s)" % (message, name, sender)

            if bot_test == '':
                try:
                    import pdb; pdb.set_trace()
                    send_mail(subject, email_message, sender, settings.CONTACT_EMAIL_RECIPIENT)
                except Exception as e:
                    print e
                    return HttpResponseRedirect('/contact')
            return HttpResponseRedirect('/about')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {
        'form': form,
    }, context_instance=RequestContext(request))
